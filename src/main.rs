use axum::{
    Router,
    extract::Json,
    http::StatusCode,
    response::{
        IntoResponse,
        sse::{Event, Sse},
    },
    routing::post,
};
use chrono::Local;
use once_cell::sync::Lazy;
use serde::{Deserialize, Serialize};
use std::convert::Infallible;
use std::{sync::Arc, time::Duration};
use tokio::{sync::Mutex, time::Instant};
use tokio_stream::wrappers::ReceiverStream;
use uuid::Uuid;

// ---------------- GLOBAL TOKEN BUCKET ----------------
// configurable thousand tokens/sec
static THOUGHPUT: Lazy<u64> = Lazy::new(|| {
    // Thousand Token per seconds
    std::env::var("THOUGHPUT")
        .unwrap_or_else(|_| "1".to_string()) // default = 1000
        .parse::<u64>()                         // parse into integer
        .expect("Invalid THOUGHPUT value")      // crash if parse fails
        * 1000 // scale up
});

// static PORT string
static PORT: Lazy<String> = Lazy::new(|| {
    // default = 8080
    std::env::var("PORT").unwrap_or_else(|_| "8080".to_string())
});

// Shared state: number of tokens available
static TOKEN_BUCKET: Lazy<Arc<Mutex<u64>>> = Lazy::new(|| Arc::new(Mutex::new(0)));

async fn token_refiller() {
    let refill_rate = *THOUGHPUT;
    let interval = Duration::from_secs(1);
    loop {
        tokio::time::sleep(interval).await;
        let mut bucket = TOKEN_BUCKET.lock().await;
        *bucket = refill_rate; // refill per second
    }
}

// Consume N tokens if available, waiting if not
async fn consume_tokens(n: u64) {
    loop {
        {
            let mut bucket = TOKEN_BUCKET.lock().await;
            if *bucket >= n {
                *bucket -= n;
                return;
            }
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
}

//
// ---------------- REQUEST / RESPONSE STRUCTS ----------------
//

#[derive(Debug, Deserialize)]
struct ChatRequest {
    model: String,
    messages: Vec<ChatMessage>,
    #[serde(default)]
    max_tokens: Option<u64>,
    #[serde(default)]
    stream: bool,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
struct ChatMessage {
    role: String,
    content: String,
}

#[derive(Debug, Serialize)]
struct ChatResponse {
    id: String,
    object: String,
    created: u64,
    choices: Vec<Choice>,
    usage: Usage,
}

#[derive(Debug, Serialize)]
struct Choice {
    index: u32,
    message: ChatMessage,
    finish_reason: String,
}

#[derive(Debug, Serialize)]
struct Usage {
    prompt_tokens: u64,
    completion_tokens: u64,
    total_tokens: u64,
}

//
// ---------------- HANDLER ----------------
//

async fn chat_completions(Json(req): Json<ChatRequest>) -> impl IntoResponse {
    if req.stream {
        // STREAMING MODE
        let (tx, rx) = tokio::sync::mpsc::channel::<Result<Event, Infallible>>(10);

        let completion_len = req.max_tokens.unwrap_or(50);
        let id = Uuid::new_v4().to_string();
        println!(
            "[REQ][{}] Session {} Inference model: {}",
            Local::now().format("%H:%M:%S %z"),
            id,
            req.model,
        );

        // Spawn background task to feed events
        tokio::spawn(async move {
            for i in 0..completion_len {
                consume_tokens(1).await;
                let content = format!("tok{} ", i);

                let chunk = serde_json::json!({
                    "id": id,
                    "object": "chat.completion.chunk",
                    "choices": [{
                        "index": 0,
                        "delta": { "role": "assistant", "content": content },
                        "finish_reason": serde_json::Value::Null
                    }]
                });

                if tx
                    .send(Ok(Event::default().data(chunk.to_string())))
                    .await
                    .is_err()
                {
                    return;
                }
            }

            // Final done event
            let _ = tx.send(Ok(Event::default().data("[DONE]"))).await;
            println!(
                "[FIN][{}] Session {} completed",
                Local::now().format("%H:%M:%S %z"),
                id,
            )
        });

        Sse::new(ReceiverStream::new(rx)).into_response()
    } else {
        // NORMAL AGGREGATED RESPONSE
        let completion_len = req.max_tokens.unwrap_or(50);
        let mut output = String::new();

        for i in 0..completion_len {
            consume_tokens(1).await;
            output.push_str(&format!("tok{} ", i));
        }

        let resp = ChatResponse {
            id: Uuid::new_v4().to_string(),
            object: "chat.completion".to_string(),
            created: Instant::now().elapsed().as_secs(),
            choices: vec![Choice {
                index: 0,
                message: ChatMessage {
                    role: "assistant".to_string(),
                    content: output.trim().to_string(),
                },
                finish_reason: "stop".to_string(),
            }],
            usage: Usage {
                prompt_tokens: req.messages.len() as u64 * 10,
                completion_tokens: completion_len,
                total_tokens: req.messages.len() as u64 * 10 + completion_len,
            },
        };

        (StatusCode::OK, axum::Json(resp)).into_response()
    }
}

//
// ---------------- BOOTSTRAP ----------------
//

#[tokio::main]
async fn main() {
    tokio::spawn(token_refiller());

    let app = Router::new().route("/v1/chat/completions", post(chat_completions));
    // HOST_ON = HOST + PORT
    // let host_on = format!("{}:{}", "0.0.0.0", PORT);
    // once_cell::sync::Lazy<std::string::String>` cannot be formatted with the default formatter
    let host_on = format!("{}:{}", "0.0.0.0", PORT.to_string());
    let listener = tokio::net::TcpListener::bind(host_on).await.unwrap();

    println!(
        "🚀 Dummy LLM API running on {} (tokens/s = {})",
        listener.local_addr().unwrap(),
        *THOUGHPUT
    );

    axum::serve(listener, app).await.unwrap();
}

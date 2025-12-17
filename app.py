#!/usr/bin/env python3
"""
Dummy OpenAI API Server

A mock implementation of the OpenAI API that returns realistic dummy responses
for testing and development purposes.

Endpoints:
- POST /v1/chat/completions - Chat completion responses
- POST /v1/embeddings - Text embedding responses
- GET /v1/models - List available models
- GET /v1/models/{id} - Get specific model info

Usage:
    python app.py

Environment variables:
    PORT - Port to run the server on (default: 8000)
    API_KEY - Required API key for authentication (default: sk-dummy)
"""

import os
import json
import time
import random
import datetime
from typing import List, Dict, Any, Optional
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', 8000))
REQUIRED_API_KEY = os.getenv('API_KEY', 'sk-dummy')

# Dummy model data
AVAILABLE_MODELS = [
    {
        "id": "gpt-4",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai"
    },
    {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1677610603,
        "owned_by": "openai"
    },
    {
        "id": "text-embedding-ada-002",
        "object": "model",
        "created": 1677610604,
        "owned_by": "openai"
    },
    {
        "id": "gpt-4-turbo",
        "object": "model",
        "created": 1700538000,
        "owned_by": "openai"
    }
]

# Dummy responses for different scenarios
DUMMY_CHAT_RESPONSES = [
    "Hello! I'm an AI assistant powered by dummy data. How can I help you today?",
    "That's an interesting question! Based on my training, I would say that...",
    "I understand your concern. Let me think about this carefully...",
    "Here are some thoughts on that topic:\n\n1. First consideration\n2. Second point\n3. Finally...",
    "I can help you with that! Here's what I recommend based on the information provided."
]

DUMMY_EMBEDDINGS = [
    [0.1, -0.2, 0.3, 0.4, -0.5, 0.6, -0.7, 0.8],
    [-0.9, 0.1, -0.2, 0.3, -0.4, 0.5, -0.6, 0.7],
    [0.2, 0.3, -0.4, 0.5, -0.6, 0.7, -0.8, 0.9]
]

def check_api_key() -> tuple[bool, Optional[str]]:
    """Check if the provided API key is valid."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False, "Missing or invalid Authorization header"

    provided_key = auth_header[7:]  # Remove 'Bearer ' prefix
    if provided_key != REQUIRED_API_KEY:
        return False, "Invalid API key"

    return True, None

def create_chat_completion(messages: List[Dict], model: str, **kwargs) -> Dict[str, Any]:
    """Create a dummy chat completion response."""
    # Extract the last user message
    user_message = ""
    for msg in reversed(messages):
        if msg.get('role') == 'user':
            user_message = msg.get('content', '')
            break

    # Choose a response based on the message content
    response_text = random.choice(DUMMY_CHAT_RESPONSES)

    # Add some context-aware responses
    if any(word in user_message.lower() for word in ['code', 'programming', 'function']):
        response_text = "Here's some example code:\n\n```python\ndef hello_world():\n    print('Hello, World!')\n    return 'Success'\n```\n\nIs this what you're looking for?"
    elif any(word in user_message.lower() for word in ['help', 'assist']):
        response_text = "I'm here to help! I can assist with a wide variety of tasks including answering questions, writing, coding, and problem-solving. What specifically would you like help with?"
    elif any(word in user_message.lower() for word in ['summarize', 'summary']):
        response_text = "Based on the text provided, here's a summary of the key points:\n\n- Main topic: The content discusses important concepts\n- Key findings: Multiple insights were presented\n- Conclusion: The information suggests several implications\n\nWould you like me to elaborate on any of these points?"

    return {
        "id": f"chatcmpl-{random.randint(100000, 999999)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": sum(len(msg.get('content', '').split()) for msg in messages),
            "completion_tokens": len(response_text.split()),
            "total_tokens": sum(len(msg.get('content', '').split()) for msg in messages) + len(response_text.split())
        }
    }

def create_embedding_response(text: str, model: str) -> Dict[str, Any]:
    """Create a dummy embedding response."""
    # Simulate embedding generation time
    time.sleep(0.1)

    # Generate or select a dummy embedding vector
    embedding_dim = 1536  # OpenAI ada-002 dimension
    embedding = [random.uniform(-1, 1) for _ in range(embedding_dim)]

    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": embedding,
                "index": 0
            }
        ],
        "model": model,
        "usage": {
            "prompt_tokens": len(text.split()),
            "total_tokens": len(text.split())
        }
    }

@app.route('/v1/models', methods=['GET'])
def list_models():
    """List all available models."""
    is_valid, error = check_api_key()
    if not is_valid:
        return jsonify({"error": {"message": error, "type": "unauthorized"}}), 401

    return jsonify({
        "object": "list",
        "data": AVAILABLE_MODELS
    })

@app.route('/v1/models/<model_id>', methods=['GET'])
def get_model(model_id: str):
    """Get information about a specific model."""
    is_valid, error = check_api_key()
    if not is_valid:
        return jsonify({"error": {"message": error, "type": "unauthorized"}}), 401

    model = next((m for m in AVAILABLE_MODELS if m["id"] == model_id), None)
    if not model:
        return jsonify({"error": {"message": "Model not found", "type": "not_found"}}), 404

    return jsonify(model)

@app.route('/v1/chat/completions', methods=['POST'])
def create_completion():
    """Create a chat completion."""
    is_valid, error = check_api_key()
    if not is_valid:
        return jsonify({"error": {"message": error, "type": "unauthorized"}}), 401

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": {"message": "Request body is required", "type": "invalid_request"}}), 400

        messages = data.get('messages', [])
        model = data.get('model', 'gpt-3.5-turbo')
        max_tokens = data.get('max_tokens', 150)
        temperature = data.get('temperature', 0.7)
        stream = data.get('stream', False)

        if not messages:
            return jsonify({"error": {"message": "messages is required", "type": "invalid_request"}}), 400

        # Simulate processing time
        processing_delay = random.uniform(0.5, 2.0)
        time.sleep(processing_delay)

        if stream:
            # For streaming responses, we'll return Server-Sent Events
            def generate():
                response = create_chat_completion(messages, model)
                content = response["choices"][0]["message"]["content"]

                # Stream the response character by character
                current_content = ""
                for i, char in enumerate(content):
                    current_content += char
                    chunk = {
                        "id": response["id"],
                        "object": "chat.completion.chunk",
                        "created": response["created"],
                        "model": model,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": char},
                                "finish_reason": None
                            }
                        ]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    time.sleep(0.01)  # Small delay to simulate streaming

                # Send final chunk
                final_chunk = {
                    "id": response["id"],
                    "object": "chat.completion.chunk",
                    "created": response["created"],
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ]
                }
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return Response(generate(), mimetype='text/plain')

        else:
            response = create_chat_completion(messages, model)
            return jsonify(response)

    except Exception as e:
        return jsonify({"error": {"message": str(e), "type": "internal_server_error"}}), 500

@app.route('/v1/embeddings', methods=['POST'])
def create_embeddings():
    """Create embeddings for text."""
    is_valid, error = check_api_key()
    if not is_valid:
        return jsonify({"error": {"message": error, "type": "unauthorized"}}), 401

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": {"message": "Request body is required", "type": "invalid_request"}}), 400

        input_text = data.get('input', '')
        model = data.get('model', 'text-embedding-ada-002')

        if not input_text:
            return jsonify({"error": {"message": "input is required", "type": "invalid_request"}}), 400

        # Handle both single text and array of texts
        if isinstance(input_text, str):
            texts = [input_text]
        elif isinstance(input_text, list):
            texts = input_text
        else:
            return jsonify({"error": {"message": "input must be string or array of strings", "type": "invalid_request"}}), 400

        # Generate embeddings for all texts
        data_items = []
        for i, text in enumerate(texts):
            embedding_dim = 1536
            embedding = [random.uniform(-1, 1) for _ in range(embedding_dim)]
            data_items.append({
                "object": "embedding",
                "embedding": embedding,
                "index": i
            })

        total_tokens = sum(len(text.split()) for text in texts)

        return jsonify({
            "object": "list",
            "data": data_items,
            "model": model,
            "usage": {
                "prompt_tokens": total_tokens,
                "total_tokens": total_tokens
            }
        })

    except Exception as e:
        return jsonify({"error": {"message": str(e), "type": "internal_server_error"}}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        "message": "Dummy OpenAI API Server",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat_completions": "/v1/chat/completions",
            "embeddings": "/v1/embeddings",
            "health": "/health"
        },
        "api_key": REQUIRED_API_KEY,
        "documentation": "https://platform.openai.com/docs/api-reference"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": {"message": "Endpoint not found", "type": "not_found"}}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": {"message": "Method not allowed", "type": "method_not_allowed"}}), 405

if __name__ == '__main__':
    print(f"Starting Dummy OpenAI API Server on port {PORT}")
    print(f"Required API Key: {REQUIRED_API_KEY}")
    print(f"Server running at: http://localhost:{PORT}")
    print("\nAvailable endpoints:")
    print("  GET  /v1/models - List models")
    print("  POST /v1/chat/completions - Chat completions")
    print("  POST /v1/embeddings - Create embeddings")
    print("  GET  /health - Health check")
    print("\nExample usage:")
    print("  curl -H 'Authorization: Bearer sk-dummy' http://localhost:8000/v1/models")
    print("  curl -X POST -H 'Authorization: Bearer sk-dummy' -H 'Content-Type: application/json' \\")
    print("    -d '{\"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}], \"model\": \"gpt-3.5-turbo\"}' \\")
    print("    http://localhost:8000/v1/chat/completions")

    app.run(host='0.0.0.0', port=PORT, debug=True)

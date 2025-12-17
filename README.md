# Dummy OpenAI API

A comprehensive mock implementation of the OpenAI API for testing and development purposes. This dummy API provides realistic responses without making actual API calls to OpenAI's servers, making it perfect for development, testing, and educational purposes.

## 🚀 Features

- **Full OpenAI API Compatibility**: Implements key OpenAI API endpoints with realistic responses
- **Multiple Models Support**: Supports various dummy models including GPT-3.5, GPT-4, and embedding models
- **Streaming Responses**: Supports Server-Sent Events (SSE) for streaming chat completions
- **Context-Aware Responses**: Generates responses based on input context (coding, help, summarization)
- **Realistic Token Usage**: Reports plausible token counts and usage statistics
- **Authentication**: API key-based authentication (default: `sk-dummy`)
- **Error Handling**: Comprehensive error responses matching OpenAI's format
- **Cross-Origin Support**: CORS enabled for web applications
- **Health Monitoring**: Built-in health check endpoint

## 📋 API Endpoints

### Models
- `GET /v1/models` - List available models
- `GET /v1/models/{id}` - Get specific model information

### Chat Completions
- `POST /v1/chat/completions` - Generate chat completions
  - Supports streaming via Server-Sent Events
  - Multiple response formats
  - Context-aware responses

### Embeddings
- `POST /v1/embeddings` - Create text embeddings
  - Single or batch text embedding
  - 1536-dimensional vectors (matching OpenAI ada-002)

### Utility
- `GET /health` - Health check endpoint
- `GET /` - API information and documentation

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. **Clone or download the dummy API files**
   ```bash
   cd dummy-openai-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python app.py
   ```

4. **Verify installation**
   ```bash
   curl http://localhost:8000/health
   ```

The server will start on `http://localhost:8000` by default.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `API_KEY` | Required API key | `sk-dummy` |

### Usage Examples

```bash
# Start server on port 3000
PORT=3000 python app.py

# Use custom API key
API_KEY=my-custom-key python app.py
```

## 🔑 Authentication

All API requests require a valid API key in the Authorization header:

```bash
curl -H "Authorization: Bearer sk-dummy" \
     http://localhost:8000/v1/models
```

## 📖 API Reference

### Chat Completions

#### Basic Usage
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 150,
    "temperature": 0.7
  }'
```

#### Streaming Response
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }'
```

#### Response Format
```json
{
  "id": "chatcmpl-123456",
  "object": "chat.completion",
  "created": 1699000000,
  "model": "gpt-3.5-turbo",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 9,
    "total_tokens": 14
  }
}
```

### Embeddings

#### Single Text
```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer sk-dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "Sample text for embedding"
  }'
```

#### Multiple Texts
```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer sk-dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": [
      "First text",
      "Second text",
      "Third text"
    ]
  }'
```

#### Response Format
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.1, -0.2, 0.3, ...],
      "index": 0
    }
  ],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 3,
    "total_tokens": 3
  }
}
```

### Models

#### List Models
```bash
curl -H "Authorization: Bearer sk-dummy" \
     http://localhost:8000/v1/models
```

#### Get Specific Model
```bash
curl -H "Authorization: Bearer sk-dummy" \
     http://localhost:8000/v1/models/gpt-3.5-turbo
```

## 🐍 Python Client Examples

### Using Requests Library
```python
import requests

API_BASE_URL = "http://localhost:8000/v1"
API_KEY = "sk-dummy"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Chat completion
response = requests.post(
    f"{API_BASE_URL}/chat/completions",
    headers=headers,
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 100
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Using OpenAI Client Library
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-dummy",
    base_url="http://localhost:8000/v1"
)

# Chat completion
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=100
)

print(completion.choices[0].message.content)
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python client_example.py
```

This will test:
- ✅ Model listing
- ✅ Chat completions
- ✅ Streaming responses
- ✅ Embeddings creation
- ✅ Error handling
- ✅ Performance metrics
- ✅ OpenAI client compatibility

### Individual Tests
```bash
# Health check
curl http://localhost:8000/health

# List models
curl -H "Authorization: Bearer sk-dummy" \
     http://localhost:8000/v1/models

# Test chat completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-dummy" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## 🔧 Development

### Available Models
- `gpt-3.5-turbo` - General purpose chat model
- `gpt-4` - Advanced chat model
- `gpt-4-turbo` - Latest turbo model
- `text-embedding-ada-002` - Text embedding model

### Customization

#### Adding New Dummy Responses
Edit the `DUMMY_CHAT_RESPONSES` list in `app.py`:

```python
DUMMY_CHAT_RESPONSES = [
    "Your custom response here",
    "Another response option",
    # ... more responses
]
```

#### Adding Context-Aware Responses
Extend the `create_chat_completion` function:

```python
if any(word in user_message.lower() for word in ['your', 'keywords']):
    response_text = "Your custom response based on keywords"
```

#### Adding New Models
Add to the `AVAILABLE_MODELS` list:

```python
AVAILABLE_MODELS = [
    {
        "id": "your-custom-model",
        "object": "model",
        "created": int(time.time()),
        "owned_by": "your-org"
    },
    # ... existing models
]
```

## 🐛 Error Handling

The API returns standard HTTP status codes and error formats:

### 400 Bad Request
```json
{
  "error": {
    "message": "messages is required",
    "type": "invalid_request"
  }
}
```

### 401 Unauthorized
```json
{
  "error": {
    "message": "Invalid API key",
    "type": "unauthorized"
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "message": "Model not found",
    "type": "not_found"
  }
}
```

## 📊 Performance

The dummy API is designed to simulate realistic processing times:
- **Chat Completions**: 0.5-2.0 seconds response time
- **Embeddings**: ~0.1 seconds processing time
- **Models**: Instant response
- **Streaming**: 0.01 second intervals between chunks

## 🔒 Security Notes

⚠️ **This is a dummy implementation for testing only!**

- Do not use in production environments
- API key validation is basic (exact match)
- No rate limiting implemented
- No data persistence or privacy protections
- All responses are generated locally

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and testing purposes. Use at your own risk.

## 🆘 Support

For issues or questions:
1. Check the examples in `client_example.py`
2. Verify server is running: `curl http://localhost:8000/health`
3. Check API key configuration
4. Review error messages for debugging

## 🎯 Use Cases

### Development & Testing
- Test applications without OpenAI API costs
- Develop features offline
- Create consistent test environments

### Education & Learning
- Learn OpenAI API integration
- Understand API response formats
- Practice with AI/ML concepts

### CI/CD Pipelines
- Automated testing without API dependencies
- Consistent test environments
- Faster test execution

### Prototyping
- Rapid prototyping of AI features
- UI/UX development with realistic data
- Proof of concept demonstrations

---

**Happy coding! 🚀**
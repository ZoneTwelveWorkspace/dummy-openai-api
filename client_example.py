# client_example.py
"""
Client Example for Dummy OpenAI API

This file demonstrates how to interact with the Dummy OpenAI API
using both the OpenAI Python client library and direct HTTP requests.

Prerequisites:
1. Start the dummy API server: python app.py
2. Install requirements: pip install -r requirements.txt
3. Install OpenAI client: pip install openai
"""

import requests
import json
import time
from typing import List, Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000/v1"
API_KEY = "sk-dummy"  # Default dummy API key
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_models_endpoint():
    """Test the models endpoint."""
    print("=" * 50)
    print("Testing Models Endpoint")
    print("=" * 50)

    response = requests.get(f"{API_BASE_URL}/models", headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        print("✓ Successfully retrieved models:")
        for model in data["data"]:
            print(f"  - {model['id']} (owned by {model['owned_by']})")
    else:
        print(f"✗ Failed to get models: {response.status_code}")
        print(response.json())

def test_chat_completion():
    """Test basic chat completion."""
    print("\n" + "=" * 50)
    print("Testing Chat Completion")
    print("=" * 50)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello! Can you help me with Python programming?"}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print("✓ Chat completion successful:")
        print(f"  Model: {data['model']}")
        print(f"  Response: {data['choices'][0]['message']['content']}")
        print(f"  Usage: {data['usage']}")
    else:
        print(f"✗ Chat completion failed: {response.status_code}")
        print(response.json())

def test_chat_completion_streaming():
    """Test streaming chat completion."""
    print("\n" + "=" * 50)
    print("Testing Streaming Chat Completion")
    print("=" * 50)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Write a short poem about code."}
        ],
        "stream": True
    }

    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload,
        stream=True
    )

    if response.status_code == 200:
        print("✓ Streaming response:")
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        if 'choices' in chunk and chunk['choices']:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                print(delta['content'], end='', flush=True)
                    except json.JSONDecodeError:
                        continue
        print("\n✓ Streaming completed")
    else:
        print(f"✗ Streaming failed: {response.status_code}")

def test_embeddings():
    """Test embeddings creation."""
    print("\n" + "=" * 50)
    print("Testing Embeddings")
    print("=" * 50)

    # Test single text embedding
    payload = {
        "model": "text-embedding-ada-002",
        "input": "This is a sample text for embedding."
    }

    response = requests.post(
        f"{API_BASE_URL}/embeddings",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print("✓ Single text embedding successful:")
        print(f"  Model: {data['model']}")
        print(f"  Embedding dimension: {len(data['data'][0]['embedding'])}")
        print(f"  First 5 values: {data['data'][0]['embedding'][:5]}")
        print(f"  Usage: {data['usage']}")
    else:
        print(f"✗ Single embedding failed: {response.status_code}")
        print(response.json())

    # Test multiple text embeddings
    payload = {
        "model": "text-embedding-ada-002",
        "input": [
            "First text for embedding.",
            "Second text for embedding.",
            "Third text for embedding."
        ]
    }

    response = requests.post(
        f"{API_BASE_URL}/embeddings",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print("✓ Multiple text embeddings successful:")
        print(f"  Number of embeddings: {len(data['data'])}")
        for i, item in enumerate(data['data']):
            print(f"  Embedding {i}: dimension {len(item['embedding'])}, first 3 values: {item['embedding'][:3]}")
    else:
        print(f"✗ Multiple embeddings failed: {response.status_code}")

def test_context_aware_responses():
    """Test context-aware responses based on input."""
    print("\n" + "=" * 50)
    print("Testing Context-Aware Responses")
    print("=" * 50)

    test_cases = [
        {
            "role": "user",
            "content": "Can you help me write a Python function to calculate fibonacci numbers?"
        },
        {
            "role": "user",
            "content": "Please summarize this document for me."
        },
        {
            "role": "user",
            "content": "I need assistance with my project."
        }
    ]

    for i, message in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {message['content']}")

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [message],
            "max_tokens": 100
        }

        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=HEADERS,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            response_content = data['choices'][0]['message']['content']
            print(f"  Response: {response_content[:100]}{'...' if len(response_content) > 100 else ''}")
        else:
            print(f"  ✗ Failed: {response.status_code}")

def test_error_handling():
    """Test error handling scenarios."""
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)

    # Test invalid API key
    print("\n1. Testing invalid API key:")
    invalid_headers = {
        "Authorization": "Bearer invalid-key",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}]
    }

    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        headers=invalid_headers,
        json=payload
    )

    if response.status_code == 401:
        print("  ✓ Correctly rejected invalid API key")
        error_data = response.json()
        print(f"  Error: {error_data['error']['message']}")
    else:
        print(f"  ✗ Expected 401, got {response.status_code}")

    # Test missing required fields
    print("\n2. Testing missing required fields:")
    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        headers=HEADERS,
        json={}  # Empty payload
    )

    if response.status_code == 400:
        print("  ✓ Correctly rejected missing fields")
        error_data = response.json()
        print(f"  Error: {error_data['error']['message']}")
    else:
        print(f"  ✗ Expected 400, got {response.status_code}")

def openai_client_comparison():
    """Compare with actual OpenAI client usage."""
    print("\n" + "=" * 50)
    print("OpenAI Client Comparison")
    print("=" * 50)

    try:
        from openai import OpenAI

        # Configure OpenAI client to use dummy API
        client = OpenAI(
            api_key=API_KEY,
            base_url=f"{API_BASE_URL}/../"  # Remove /v1 to get base URL
        )

        # Test chat completion
        print("\n1. Using OpenAI client for chat completion:")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello from OpenAI client!"}
            ],
            max_tokens=50
        )

        print(f"  ✓ Response: {completion.choices[0].message.content}")
        print(f"  ✓ Model: {completion.model}")
        print(f"  ✓ Usage: {completion.usage}")

    except ImportError:
        print("\nOpenAI client library not installed. Install with:")
        print("  pip install openai")
    except Exception as e:
        print(f"\n✗ OpenAI client test failed: {e}")

def test_health_endpoint():
    """Test health check endpoint."""
    print("\n" + "=" * 50)
    print("Testing Health Endpoint")
    print("=" * 50)

    response = requests.get("http://localhost:8000/health")

    if response.status_code == 200:
        data = response.json()
        print("✓ Health check successful:")
        print(f"  Status: {data['status']}")
        print(f"  Version: {data['version']}")
        print(f"  Timestamp: {data['timestamp']}")
    else:
        print(f"✗ Health check failed: {response.status_code}")

def performance_test():
    """Simple performance test."""
    print("\n" + "=" * 50)
    print("Performance Test")
    print("=" * 50)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Quick response test"}],
        "max_tokens": 50
    }

    # Test multiple requests
    num_requests = 5
    start_time = time.time()

    for i in range(num_requests):
        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=HEADERS,
            json=payload
        )

        if response.status_code == 200:
            print(f"  Request {i+1}: ✓")
        else:
            print(f"  Request {i+1}: ✗ {response.status_code}")

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_requests

    print(f"\n✓ Performance Results:")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average per request: {avg_time:.2f}s")
    print(f"  Requests per second: {num_requests/total_time:.1f}")

def main():
    """Run all tests."""
    print("Dummy OpenAI API - Client Examples")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY}")
    print("=" * 60)

    # Check if server is running
    try:
        requests.get("http://localhost:8000/health", timeout=2)
    except requests.RequestException:
        print("❌ Cannot connect to server. Make sure the dummy API server is running:")
        print("   python app.py")
        return

    # Run all tests
    test_health_endpoint()
    test_models_endpoint()
    test_chat_completion()
    test_context_aware_responses()
    test_embeddings()
    test_error_handling()
    test_chat_completion_streaming()
    openai_client_comparison()
    performance_test()

    print("\n" + "=" * 60)
    print("All tests completed! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    main()

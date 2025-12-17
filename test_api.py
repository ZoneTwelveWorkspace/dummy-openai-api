#!/usr/bin/env python3
"""
Simple API Test Script

Quick test script to verify the dummy OpenAI API installation and basic functionality.
This script checks if the server is running and tests key endpoints.

Usage:
    python test_api.py

Requirements:
    - Dummy API server should be running on localhost:8000
    - requests library (pip install requests)
"""

import sys
import json
import time
from typing import Dict, Any, Optional

def test_imports():
    """Test if required libraries are available."""
    try:
        import requests
        print("✓ requests library available")
        return True
    except ImportError:
        print("✗ requests library not found. Install with: pip install requests")
        return False

def test_server_connectivity() -> bool:
    """Test if the API server is running and accessible."""
    try:
        import requests

        print("\nTesting server connectivity...")
        response = requests.get("http://localhost:8000/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server is running - Status: {data.get('status', 'unknown')}")
            print(f"  Version: {data.get('version', 'unknown')}")
            print(f"  Timestamp: {data.get('timestamp', 'unknown')}")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False

    except requests.ConnectionError:
        print("✗ Cannot connect to server. Make sure the dummy API is running:")
        print("  python app.py")
        return False
    except requests.Timeout:
        print("✗ Server connection timed out")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def test_authentication() -> bool:
    """Test API authentication."""
    import requests

    print("\nTesting authentication...")

    # Test with invalid API key
    headers_invalid = {
        "Authorization": "Bearer invalid-key",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "test"}]
    }

    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        headers=headers_invalid,
        json=payload,
        timeout=5
    )

    if response.status_code == 401:
        print("✓ Authentication working - correctly rejected invalid key")
        return True
    else:
        print(f"✗ Authentication test failed - expected 401, got {response.status_code}")
        return False

def test_models_endpoint() -> bool:
    """Test the models listing endpoint."""
    import requests

    print("\nTesting models endpoint...")

    headers = {
        "Authorization": "Bearer sk-dummy",
        "Content-Type": "application/json"
    }

    response = requests.get(
        "http://localhost:8000/v1/models",
        headers=headers,
        timeout=5
    )

    if response.status_code == 200:
        data = response.json()
        models = data.get("data", [])
        print(f"✓ Models endpoint working - Found {len(models)} models:")
        for model in models:
            print(f"  - {model['id']}")
        return True
    else:
        print(f"✗ Models endpoint failed - Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return False

def test_chat_completion() -> bool:
    """Test basic chat completion functionality."""
    import requests

    print("\nTesting chat completion...")

    headers = {
        "Authorization": "Bearer sk-dummy",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello! Please respond with exactly: API Test Successful"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            print("✓ Chat completion working")
            print(f"  Model: {data.get('model', 'unknown')}")
            print(f"  Response: {content}")
            print(f"  Usage: {usage}")
            return True
        else:
            print(f"✗ Chat completion failed - Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"✗ Chat completion error: {e}")
        return False

def test_embeddings() -> bool:
    """Test embeddings creation."""
    import requests

    print("\nTesting embeddings...")

    headers = {
        "Authorization": "Bearer sk-dummy",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "text-embedding-ada-002",
        "input": "This is a test sentence for embedding generation."
    }

    try:
        response = requests.post(
            "http://localhost:8000/v1/embeddings",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            embedding = data["data"][0]["embedding"]

            print("✓ Embeddings working")
            print(f"  Model: {data.get('model', 'unknown')}")
            print(f"  Embedding dimension: {len(embedding)}")
            print(f"  First 5 values: {embedding[:5]}")
            print(f"  Usage: {data.get('usage', {})}")
            return True
        else:
            print(f"✗ Embeddings failed - Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"✗ Embeddings error: {e}")
        return False

def test_streaming() -> bool:
    """Test streaming chat completion."""
    import requests

    print("\nTesting streaming response...")

    headers = {
        "Authorization": "Bearer sk-dummy",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Count from 1 to 5"}
        ],
        "stream": True,
        "max_tokens": 20
    }

    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=15
        )

        if response.status_code == 200:
            print("✓ Streaming working")
            chunk_count = 0

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
                                    chunk_count += 1
                        except json.JSONDecodeError:
                            continue

            print(f"  Received {chunk_count} streaming chunks")
            return True
        else:
            print(f"✗ Streaming failed - Status: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Streaming error: {e}")
        return False

def test_error_handling() -> bool:
    """Test error handling scenarios."""
    import requests

    print("\nTesting error handling...")

    headers = {
        "Authorization": "Bearer sk-dummy",
        "Content-Type": "application/json"
    }

    # Test missing required fields
    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        headers=headers,
        json={},  # Empty payload
        timeout=5
    )

    if response.status_code == 400:
        print("✓ Error handling working - correctly rejected empty payload")
        return True
    else:
        print(f"✗ Error handling test failed - expected 400, got {response.status_code}")
        return False

def print_summary(test_results: Dict[str, bool]):
    """Print a summary of all test results."""
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(test_results.values())
    total = len(test_results)

    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        icon = "✓" if result else "✗"
        print(f"{icon} {test_name:<30} {status}")

    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your dummy OpenAI API is working correctly.")
        print("\nNext steps:")
        print("- Check out client_example.py for more comprehensive examples")
        print("- Try the API with your own applications")
        print("- Customize responses in config.py")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("\nCommon solutions:")
        print("- Make sure the server is running: python app.py")
        print("- Check that port 8000 is not blocked")
        print("- Verify all dependencies are installed: pip install -r requirements.txt")

def main():
    """Run all tests."""
    print("Dummy OpenAI API - Installation Test")
    print("=" * 50)
    print("This script will test your dummy OpenAI API installation.")
    print("Make sure the server is running before starting tests.")
    print("=" * 50)

    # Run tests
    test_results = {}

    # Test imports first
    if not test_imports():
        print("\n❌ Setup failed. Please install required dependencies.")
        sys.exit(1)

    # Run connectivity test
    test_results["Server Connectivity"] = test_server_connectivity()

    # Only continue if server is accessible
    if not test_results["Server Connectivity"]:
        print_summary(test_results)
        sys.exit(1)

    # Run other tests
    test_results["Authentication"] = test_authentication()
    test_results["Models Endpoint"] = test_models_endpoint()
    test_results["Chat Completion"] = test_chat_completion()
    test_results["Embeddings"] = test_embeddings()
    test_results["Streaming"] = test_streaming()
    test_results["Error Handling"] = test_error_handling()

    # Print summary
    print_summary(test_results)

    # Exit with appropriate code
    if all(test_results.values()):
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed

if __name__ == "__main__":
    main()

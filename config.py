# config.py
"""
Configuration settings for the Dummy OpenAI API

This file contains all configurable parameters for the dummy API server,
including model definitions, response templates, timing settings, and
other customizable behavior.
"""

import os
import datetime

# =============================================================================
# Server Configuration
# =============================================================================

# Server settings
DEFAULT_PORT = int(os.getenv('PORT', 8000))
DEFAULT_API_KEY = os.getenv('API_KEY', 'sk-dummy')
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

# Host configuration
HOST = os.getenv('HOST', '0.0.0.0')

# =============================================================================
# Model Configuration
# =============================================================================

# Available models in the dummy API
AVAILABLE_MODELS = [
    {
        "id": "gpt-4",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
        "permission": ["read"],
        "root": "gpt-4",
        "parent": None
    },
    {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1677610603,
        "owned_by": "openai",
        "permission": ["read"],
        "root": "gpt-3.5-turbo",
        "parent": None
    },
    {
        "id": "text-embedding-ada-002",
        "object": "model",
        "created": 1677610604,
        "owned_by": "openai",
        "permission": ["read"],
        "root": "text-embedding-ada-002",
        "parent": None
    },
    {
        "id": "gpt-4-turbo",
        "object": "model",
        "created": 1700538000,
        "owned_by": "openai",
        "permission": ["read"],
        "root": "gpt-4-turbo",
        "parent": None
    },
    {
        "id": "gpt-4o",
        "object": "model",
        "created": 1709000000,
        "owned_by": "openai",
        "permission": ["read"],
        "root": "gpt-4o",
        "parent": None
    }
]

# Model-specific settings
MODEL_SETTINGS = {
    "gpt-3.5-turbo": {
        "max_tokens": 4096,
        "context_window": 16384,
        "cost_per_1k_input_tokens": 0.0015,
        "cost_per_1k_output_tokens": 0.002,
        "default_temperature": 0.7,
        "default_max_tokens": 150
    },
    "gpt-4": {
        "max_tokens": 8192,
        "context_window": 32768,
        "cost_per_1k_input_tokens": 0.03,
        "cost_per_1k_output_tokens": 0.06,
        "default_temperature": 0.7,
        "default_max_tokens": 150
    },
    "gpt-4-turbo": {
        "max_tokens": 128000,
        "context_window": 128000,
        "cost_per_1k_input_tokens": 0.01,
        "cost_per_1k_output_tokens": 0.03,
        "default_temperature": 0.7,
        "default_max_tokens": 150
    },
    "gpt-4o": {
        "max_tokens": 128000,
        "context_window": 128000,
        "cost_per_1k_input_tokens": 0.005,
        "cost_per_1k_output_tokens": 0.015,
        "default_temperature": 0.7,
        "default_max_tokens": 150
    },
    "text-embedding-ada-002": {
        "max_tokens": 8191,
        "dimensions": 1536,
        "cost_per_1k_tokens": 0.0001
    }
}

# =============================================================================
# Response Templates and Dummy Data
# =============================================================================

# Default chat responses for general queries
DUMMY_CHAT_RESPONSES = [
    "Hello! I'm an AI assistant powered by dummy data. How can I help you today?",
    "That's an interesting question! Based on my training, I would say that...",
    "I understand your concern. Let me think about this carefully...",
    "Here are some thoughts on that topic:\n\n1. First consideration\n2. Second point\n3. Finally...",
    "I can help you with that! Here's what I recommend based on the information provided.",
    "Thank you for your question. Here's my response based on the available information:",
    "Great question! Let me break this down for you step by step.",
    "I appreciate you sharing that with me. Here's what I think:",
    "That's a complex topic. Let me provide you with a comprehensive answer:",
    "I'd be happy to assist you with that. Here's my analysis:"
]

# Code-related responses
CODE_RESPONSES = [
    "Here's some example code:\n\n```python\ndef hello_world():\n    print('Hello, World!')\n    return 'Success'\n```\n\nIs this what you're looking for?",
    "Here's a code example for your request:\n\n```python\n# Your code here\ndef process_data(data):\n    result = []\n    for item in data:\n        result.append(transform(item))\n    return result\n```\n\nWould you like me to explain any part of this?",
    "Here's a sample implementation:\n\n```javascript\nfunction processItems(items) {\n    return items.map(item => {\n        return {\n            ...item,\n            processed: true\n        };\n    });\n}\n```\n\nIs this helpful?",
    "I can help with code! Here's an example:\n\n```python\nimport os\n\ndef analyze_file(filepath):\n    if os.path.exists(filepath):\n        with open(filepath, 'r') as f:\n            content = f.read()\n        return content\n    else:\n        return 'File not found'\n```\n\nLet me know if you need something specific!"
]

# Help and assistance responses
HELP_RESPONSES = [
    "I'm here to help! I can assist with a wide variety of tasks including answering questions, writing, coding, and problem-solving. What specifically would you like help with?",
    "Of course, I'd be happy to help! I can provide assistance with:\n\n- Answering questions on various topics\n- Writing and editing text\n- Programming and debugging\n- Data analysis and explanations\n- Creative projects\n\nWhat would you like to work on?",
    "I'm ready to assist! My capabilities include:\n\n✓ Information and research\n✓ Writing and content creation\n✓ Technical support and coding\n✓ Problem-solving and analysis\n✓ Learning and explanations\n\nHow can I help you today?",
    "I'm here to support you with whatever you need! Whether it's:\n\n• Answering questions\n• Helping with projects\n• Debugging code\n• Writing assistance\n• Learning new concepts\n\nJust let me know what you'd like to work on!"
]

# Summarization responses
SUMMARY_RESPONSES = [
    "Based on the text provided, here's a summary of the key points:\n\n- Main topic: The content discusses important concepts\n- Key findings: Multiple insights were presented\n- Conclusion: The information suggests several implications\n\nWould you like me to elaborate on any of these points?",
    "Here's a concise summary of the material:\n\n**Key Takeaways:**\n1. Primary theme: The main concepts covered\n2. Important details: Supporting information and examples\n3. Actionable insights: What this means for practical application\n\nLet me know if you'd like more detail on any section.",
    "Summary of the content:\n\n**Overview:** The text presents comprehensive information about the topic.\n\n**Main Points:**\n• Essential concepts and definitions\n• Supporting evidence and examples\n• Practical applications and implications\n\n**Conclusion:** The material provides valuable insights and actionable guidance.\n\nIs there a specific aspect you'd like me to expand on?"
]

# Technical/professional responses
TECHNICAL_RESPONSES = [
    "Here's a detailed technical analysis:\n\n1. **Problem Definition:** Understanding the core requirements\n2. **Approach:** Recommended methodology and tools\n3. **Implementation:** Step-by-step process\n4. **Considerations:** Potential challenges and solutions\n\nWould you like me to elaborate on any of these areas?",
    "From a technical perspective, I recommend the following approach:\n\n• **Analysis:** Current situation assessment\n• **Strategy:** Optimal path forward\n• **Resources:** Required tools and knowledge\n• **Timeline:** Realistic implementation schedule\n\nWhat specific aspect would you like me to focus on?",
    "Here's my professional recommendation:\n\n**Current State:** Analysis of existing conditions\n**Recommended Solution:** Evidence-based approach\n**Implementation Plan:** Practical steps and milestones\n**Success Metrics:** How to measure effectiveness\n\nLet me know if you need clarification on any point."
]

# =============================================================================
# Embedding Configuration
# =============================================================================

# Default embedding dimension (OpenAI ada-002 uses 1536)
DEFAULT_EMBEDDING_DIMENSION = 1536

# Predefined embedding vectors for consistency
STATIC_EMBEDDINGS = [
    [0.1, -0.2, 0.3, 0.4, -0.5, 0.6, -0.7, 0.8],
    [-0.9, 0.1, -0.2, 0.3, -0.4, 0.5, -0.6, 0.7],
    [0.2, 0.3, -0.4, 0.5, -0.6, 0.7, -0.8, 0.9],
    [0.5, -0.1, 0.8, -0.3, 0.6, -0.4, 0.9, -0.2],
    [-0.3, 0.7, -0.5, 0.2, 0.8, -0.6, 0.1, 0.4]
]

# =============================================================================
# Timing and Performance Settings
# =============================================================================

# Response delays (in seconds)
TIMING_SETTINGS = {
    "chat_completion_min_delay": 0.5,
    "chat_completion_max_delay": 2.0,
    "embedding_delay": 0.1,
    "model_list_delay": 0.0,
    "streaming_chunk_delay": 0.01
}

# Processing time multipliers for different model types
MODEL_PROCESSING_MULTIPLIERS = {
    "gpt-3.5-turbo": 1.0,
    "gpt-4": 2.5,
    "gpt-4-turbo": 2.0,
    "gpt-4o": 1.8
}

# =============================================================================
# Content Filtering and Safety
# =============================================================================

# Keywords that trigger different response types
CONTENT_TRIGGERS = {
    "code_keywords": [
        "code", "programming", "function", "script", "algorithm",
        "debug", "syntax", "variable", "class", "method", "python",
        "javascript", "java", "c++", "html", "css", "sql", "api"
    ],
    "help_keywords": [
        "help", "assist", "support", "guidance", "advice", "tutorial",
        "explain", "teach", "learn", "understand", "confused"
    ],
    "summary_keywords": [
        "summarize", "summary", "overview", "brief", "main points",
        "key takeaways", "tldr", "extract", "highlight"
    ],
    "technical_keywords": [
        "technical", "analysis", "approach", "methodology", "strategy",
        "implementation", "architecture", "design", "best practices"
    ]
}

# =============================================================================
# Logging and Debug Settings
# =============================================================================

# Log levels: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Enable request/response logging
LOG_REQUESTS = os.getenv('LOG_REQUESTS', 'False').lower() == 'true'
LOG_RESPONSES = os.getenv('LOG_RESPONSES', 'False').lower() == 'true'

# Enable performance metrics
ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'

# =============================================================================
# Rate Limiting and Quotas
# =============================================================================

# Note: Rate limiting not implemented in this dummy version
# These settings are here for future extension
RATE_LIMIT_SETTINGS = {
    "requests_per_minute": 60,
    "tokens_per_minute": 10000,
    "requests_per_day": 1000
}

# =============================================================================
# Validation Rules
# =============================================================================

# Input validation limits
VALIDATION_LIMITS = {
    "max_messages_per_request": 50,
    "max_content_length": 32000,  # characters
    "max_input_tokens": 8192,
    "max_output_tokens": 4096,
    "max_batch_size": 100  # for embeddings
}

# =============================================================================
# Response Formatting
# =============================================================================

# Enable markdown formatting in responses
ENABLE_MARKDOWN = True

# Streaming response settings
STREAMING_SETTINGS = {
    "chunk_size": "character",  # "character" or "word"
    "include_metadata": True,
    "include_usage_in_stream": False
}

# =============================================================================
# Custom Response Templates
# =============================================================================

# You can add custom response templates based on specific patterns
CUSTOM_RESPONSE_TEMPLATES = {
    "greeting": [
        "Hello there! How can I assist you today?",
        "Hi! I'm here to help with whatever you need.",
        "Greetings! What can I do for you?"
    ],
    "goodbye": [
        "Goodbye! Feel free to come back if you need more help.",
        "Take care! Don't hesitate to reach out if you have more questions.",
        "See you later! I'm here whenever you need assistance."
    ],
    "error": [
        "I'm sorry, but I encountered an issue processing your request.",
        "There seems to be a problem. Let me try to help you differently.",
        "I apologize, but I'm having trouble understanding your request."
    ]
}

# =============================================================================
# Utility Functions
# =============================================================================

def get_model_settings(model_id: str) -> dict:
    """Get settings for a specific model."""
    return MODEL_SETTINGS.get(model_id, {})

def get_response_by_context(message: str, context: str = "general") -> str:
    """Get a response based on message context."""
    message_lower = message.lower()

    # Check for code-related content
    if any(keyword in message_lower for keyword in CONTENT_TRIGGERS["code_keywords"]):
        import random
        return random.choice(CODE_RESPONSES)

    # Check for help-related content
    if any(keyword in message_lower for keyword in CONTENT_TRIGGERS["help_keywords"]):
        import random
        return random.choice(HELP_RESPONSES)

    # Check for summary-related content
    if any(keyword in message_lower for keyword in CONTENT_TRIGGERS["summary_keywords"]):
        import random
        return random.choice(SUMMARY_RESPONSES)

    # Check for technical content
    if any(keyword in message_lower for keyword in CONTENT_TRIGGERS["technical_keywords"]):
        import random
        return random.choice(TECHNICAL_RESPONSES)

    # Default to general responses
    import random
    return random.choice(DUMMY_CHAT_RESPONSES)

def calculate_dummy_tokens(text: str) -> int:
    """Calculate approximate token count for text."""
    # Rough estimation: 1 token ≈ 4 characters for English text
    return len(text) // 4

def create_dummy_embedding(text: str, dimension: int = None) -> list:
    """Create a dummy embedding vector."""
    if dimension is None:
        dimension = DEFAULT_EMBEDDING_DIMENSION

    # Use text hash to generate consistent embeddings for same text
    import hashlib
    import random

    text_hash = hashlib.md5(text.encode()).hexdigest()
    random.seed(int(text_hash[:8], 16))  # Use first 8 chars of hash as seed

    embedding = [random.uniform(-1, 1) for _ in range(dimension)]

    # Normalize to unit length (common practice for embeddings)
    import math
    norm = math.sqrt(sum(x**2 for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]

    return embedding

def get_processing_delay(model_id: str, request_type: str = "chat") -> float:
    """Get appropriate processing delay based on model and request type."""
    import random

    if request_type == "embedding":
        base_delay = TIMING_SETTINGS["embedding_delay"]
    elif request_type == "chat":
        base_delay = random.uniform(
            TIMING_SETTINGS["chat_completion_min_delay"],
            TIMING_SETTINGS["chat_completion_max_delay"]
        )
        # Apply model multiplier
        multiplier = MODEL_PROCESSING_MULTIPLIERS.get(model_id, 1.0)
        base_delay *= multiplier
    else:
        base_delay = TIMING_SETTINGS["model_list_delay"]

    return base_delay

# =============================================================================
# Environment-specific Overrides
# =============================================================================

# Development settings
if os.getenv('ENVIRONMENT') == 'development':
    TIMING_SETTINGS.update({
        "chat_completion_min_delay": 0.1,
        "chat_completion_max_delay": 0.5,
        "embedding_delay": 0.05
    })
    DEBUG_MODE = True
    LOG_LEVEL = 'DEBUG'
    LOG_REQUESTS = True
    LOG_RESPONSES = True

# Testing settings
elif os.getenv('ENVIRONMENT') == 'testing':
    TIMING_SETTINGS.update({
        "chat_completion_min_delay": 0.01,
        "chat_completion_max_delay": 0.05,
        "embedding_delay": 0.01
    })
    LOG_LEVEL = 'WARNING'
    LOG_REQUESTS = False
    LOG_RESPONSES = False

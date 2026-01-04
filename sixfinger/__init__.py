"""
Sixfinger - AI Platform SDK
============================

Official Python SDK for Sixfinger services

Features:
  - API Client: Fast access to cloud AI models
  - Transformers: On-device language models (CPU-optimized)

Examples:

  # Cloud API
  >>> from sixfinger import API
  >>> api = API(api_key="your-key")
  >>> response = api.chat("Hello!")
  
  # On-Device Model
  >>> from sixfinger.transformers import SpeedLM
  >>> model = SpeedLM()
  >>> model.train_file('data.txt')
  >>> output = model.generate(b'Hello', length=100)
"""

__version__ = "2.0.0"
__author__ = "Sixfinger Team"
__email__ = "sixfingerdev@gmail.com"

# ===== API CLIENT (existing) =====
from .api import API, AsyncAPI, Conversation
from .errors import (
    SixfingerError,
    AuthenticationError,
    RateLimitError,
    APIError,
    TimeoutError,
    ValidationError
)
from .models import Message, ChatResponse, UsageStats, ModelInfo

__all__ = [
    # API Client
    'API',
    'AsyncAPI',
    'Conversation',
    
    # Errors
    'SixfingerError',
    'AuthenticationError',
    'RateLimitError',
    'APIError',
    'TimeoutError',
    'ValidationError',
    
    # Models
    'Message',
    'ChatResponse',
    'UsageStats',
    'ModelInfo',
    
    # Version
    '__version__',
]

# ===== ON-DEVICE TRANSFORMERS (optional) =====
# Only import if numpy is available
try:
    from . import transformers
    __all__.append('transformers')
except ImportError:
    # Transformers not installed
    # User can install with: pip install sixfinger[transformers]
    pass
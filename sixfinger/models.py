"""Sixfinger API Models"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class UsageStats:
    """Token usage statistics"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ChatResponse:
    """Chat response"""
    content: str
    model: str
    model_id: str
    usage: UsageStats
    finish_reason: str
    metadata: Dict[str, Any]

@dataclass
class Message:
    """Chat message"""
    role: str
    content: str

@dataclass
class ModelInfo:
    """Model information"""
    key: str
    name: str
    size: str
    available_plans: List[str]
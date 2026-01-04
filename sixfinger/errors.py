"""Sixfinger API Exceptions"""

class SixfingerError(Exception):
    """Base exception"""
    pass

class AuthenticationError(SixfingerError):
    """Authentication failed"""
    pass

class RateLimitError(SixfingerError):
    """Rate limit exceeded"""
    pass

class APIError(SixfingerError):
    """API error"""
    pass

class TimeoutError(SixfingerError):
    """Request timeout"""
    pass

class ValidationError(SixfingerError):
    """Validation error"""
    pass
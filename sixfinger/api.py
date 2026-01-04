"""
Sixfinger API Client (Sync + Async)
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any, Generator
from .errors import (
    SixfingerError,
    AuthenticationError,
    RateLimitError,
    APIError,
    TimeoutError,
    ValidationError
)
from .models import ChatResponse, UsageStats, ModelInfo


class API:
    """
    Sixfinger API Client (Sync)
    
    Example:
        >>> from sixfinger import API
        >>> client = API(api_key="sixfinger_xxx")
        >>> response = client.chat("Merhaba!")
        >>> print(response.content)
    """
    
    BASE_URL = "https://sfapi.pythonanywhere.com"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3
    ):
        self.api_key = api_key or os.getenv('SIXFINGER_API_KEY')
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        
        if not self.api_key:
            raise AuthenticationError(
                "API key required. Pass api_key or set SIXFINGER_API_KEY env var."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'sixfinger-python/1.0.0'
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 403:
                raise AuthenticationError("Email not verified or account disabled")
            elif response.status_code == 429:
                error_data = response.json()
                raise RateLimitError(error_data.get('message', 'Rate limit exceeded'))
            elif response.status_code >= 500:
                raise APIError(f"Server error: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                raise ValidationError(error_data.get('message', 'Request validation failed'))
            
            return response
        
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error. Check your internet.")
        except requests.exceptions.RequestException as e:
            raise SixfingerError(f"Request failed: {e}")
    
    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> ChatResponse:
        """
        Send chat message
        
        Args:
            message: Your message
            model: Model key (e.g., "qwen3-32b"). Auto if None.
            system_prompt: System prompt
            history: Conversation history
            max_tokens: Max tokens
            temperature: Creativity (0.1-2.0)
            stream: Enable streaming (returns generator)
        
        Returns:
            ChatResponse or Generator[str]
        """
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")
        
        payload = {'message': message, 'temperature': temperature}
        if model: payload['model'] = model
        if system_prompt: payload['system_prompt'] = system_prompt
        if history: payload['history'] = history
        if max_tokens: payload['max_tokens'] = max_tokens
        if stream: payload['stream'] = True
        
        if stream:
            return self._stream_chat(payload)
        
        response = self._request('POST', '/api/v1/chat', json=payload)
        data = response.json()
        
        return ChatResponse(
            content=data['response'],
            model=data['model_key'],
            model_id=data['model'],
            usage=UsageStats(
                prompt_tokens=data['usage']['prompt_tokens'],
                completion_tokens=data['usage']['completion_tokens'],
                total_tokens=data['usage']['total_tokens']
            ),
            finish_reason='stop',
            metadata={
                'model_size': data.get('model_size'),
                'model_language': data.get('model_language'),
                'attempts': data.get('attempts', 1)
            }
        )
    
    def _stream_chat(self, payload: Dict[str, Any]) -> Generator[str, None, None]:
        """Stream chat response"""
        response = self._request('POST', '/api/v1/chat', json=payload, stream=True)
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        if 'text' in data:
                            yield data['text']
                        elif 'error' in data:
                            raise APIError(data['error'])
                    except json.JSONDecodeError:
                        continue
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        response = self._request('GET', '/api/v1/stats')
        return response.json()
    
    def list_models(self) -> List[ModelInfo]:
        """List available models"""
        return [
            ModelInfo('llama-8b-instant', 'Meta Llama 3.1 8B Instant', '8B', ['free', 'starter', 'pro', 'plus']),
            ModelInfo('allam-2-7b', 'Allam 2 7B (Turkish/Arabic)', '7B', ['free', 'starter', 'pro', 'plus']),
            ModelInfo('qwen3-32b', 'Qwen3 32B (Turkish)', '32B', ['starter', 'pro', 'plus']),
            ModelInfo('llama-70b', 'Meta Llama 3.3 70B', '70B', ['starter', 'pro', 'plus']),
            ModelInfo('gpt-oss-120b', 'GPT-OSS 120B', '120B', ['pro', 'plus']),
        ]
    
    def conversation(self) -> 'Conversation':
        """Create conversation context"""
        return Conversation(self)
    
    def __repr__(self):
        return f"API(base_url='{self.base_url}')"
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.session.close()


class AsyncAPI:
    """
    Sixfinger API Client (Async)
    
    Example:
        >>> import asyncio
        >>> from sixfinger import AsyncAPI
        >>> 
        >>> async def main():
        ...     async with AsyncAPI(api_key="sixfinger_xxx") as client:
        ...         response = await client.chat("Merhaba!")
        ...         print(response.content)
        >>> 
        >>> asyncio.run(main())
    """
    
    BASE_URL = "https://sfapi.pythonanywhere.com"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60
    ):
        self.api_key = api_key or os.getenv('SIXFINGER_API_KEY')
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        
        if not self.api_key:
            raise AuthenticationError(
                "API key required. Pass api_key or set SIXFINGER_API_KEY env var."
            )
        
        self._session = None
        self._headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'sixfinger-python/1.0.0'
        }
    
    async def _get_session(self):
        """Lazy session initialization"""
        if self._session is None:
            try:
                import aiohttp
                self._session = aiohttp.ClientSession(headers=self._headers)
            except ImportError:
                raise ImportError(
                    "aiohttp required for async. Install: pip install aiohttp"
                )
        return self._session
    
    async def _request(self, method: str, endpoint: str, **kwargs):
        """Make async HTTP request"""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with session.request(method, url, timeout=self.timeout, **kwargs) as response:
                if response.status == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status == 403:
                    raise AuthenticationError("Email not verified")
                elif response.status == 429:
                    error_data = await response.json()
                    raise RateLimitError(error_data.get('message', 'Rate limit exceeded'))
                elif response.status >= 500:
                    raise APIError(f"Server error: {response.status}")
                elif response.status >= 400:
                    error_data = await response.json()
                    raise ValidationError(error_data.get('message', 'Validation failed'))
                
                return await response.json()
        
        except Exception as e:
            if isinstance(e, SixfingerError):
                raise
            raise APIError(f"Request failed: {e}")
    
    async def chat(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> ChatResponse:
        """Send chat message (async)"""
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")
        
        payload = {'message': message, 'temperature': temperature}
        if model: payload['model'] = model
        if system_prompt: payload['system_prompt'] = system_prompt
        if history: payload['history'] = history
        if max_tokens: payload['max_tokens'] = max_tokens
        
        if stream:
            raise NotImplementedError("Async streaming not yet implemented")
        
        data = await self._request('POST', '/api/v1/chat', json=payload)
        
        return ChatResponse(
            content=data['response'],
            model=data['model_key'],
            model_id=data['model'],
            usage=UsageStats(
                prompt_tokens=data['usage']['prompt_tokens'],
                completion_tokens=data['usage']['completion_tokens'],
                total_tokens=data['usage']['total_tokens']
            ),
            finish_reason='stop',
            metadata={
                'model_size': data.get('model_size'),
                'model_language': data.get('model_language'),
                'attempts': data.get('attempts', 1)
            }
        )
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics (async)"""
        return await self._request('GET', '/api/v1/stats')
    
    async def close(self):
        """Close session"""
        if self._session:
            await self._session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()
    
    def __repr__(self):
        return f"AsyncAPI(base_url='{self.base_url}')"


class Conversation:
    """Conversation context with history"""
    
    def __init__(self, client: API):
        self.client = client
        self.history: List[Dict[str, str]] = []
        self.model: Optional[str] = None
        self.system_prompt: Optional[str] = None
    
    def send(self, message: str, **kwargs) -> ChatResponse:
        """Send message in conversation"""
        response = self.client.chat(
            message=message,
            model=kwargs.get('model', self.model),
            system_prompt=kwargs.get('system_prompt', self.system_prompt),
            history=self.history,
            **{k: v for k, v in kwargs.items() if k not in ['model', 'system_prompt']}
        )
        
        self.history.append({'role': 'user', 'content': message})
        self.history.append({'role': 'assistant', 'content': response.content})
        
        return response
    
    def set_model(self, model: str):
        """Set default model"""
        self.model = model
        return self
    
    def set_system_prompt(self, prompt: str):
        """Set system prompt"""
        self.system_prompt = prompt
        return self
    
    def clear(self):
        """Clear history"""
        self.history = []
        return self
    
    def __repr__(self):
        return f"Conversation(messages={len(self.history)//2})"
"""
Sixfinger API Client (Sync + Async)
OpenAI-compatible API v1 client.
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any, Generator, Union
from .errors import (
    SixfingerError,
    AuthenticationError,
    RateLimitError,
    APIError,
    TimeoutError,
    ValidationError
)
from .models import ChatResponse, UsageStats, ModelInfo, Message


def _build_messages(
    message: str,
    system_prompt: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, str]]:
    """Build OpenAI-compatible messages list from legacy arguments."""
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        for msg in history:
            if "role" in msg and "content" in msg:
                messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})
    return messages


def _parse_error(response: requests.Response) -> str:
    """Extract error message from OpenAI-compatible error response."""
    try:
        data = response.json()
        if "error" in data:
            err = data["error"]
            if isinstance(err, dict):
                return err.get("message", str(err))
            return str(err)
        return response.text or f"HTTP {response.status_code}"
    except Exception:
        return response.text or f"HTTP {response.status_code}"


class API:
    """
    Sixfinger API Client (Sync)

    Example:
        >>> from sixfinger import API
        >>> client = API(api_key="sixfinger_xxx")
        >>> response = client.chat("Merhaba!")
        >>> print(response.content)
    """

    BASE_URL = "https://api.sixfinger.live"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 120,
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
            'User-Agent': 'sixfinger-python/2.1.1'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)

            if response.status_code == 401:
                raise AuthenticationError(_parse_error(response))
            elif response.status_code == 403:
                raise AuthenticationError(_parse_error(response))
            elif response.status_code == 429:
                raise RateLimitError(_parse_error(response))
            elif response.status_code >= 500:
                raise APIError(f"Server error {response.status_code}: {_parse_error(response)}")
            elif response.status_code >= 400:
                raise ValidationError(_parse_error(response))

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
        top_p: Optional[float] = None,
        stream: bool = False
    ) -> Union[ChatResponse, Generator[str, None, None]]:
        """
        Send chat message (legacy-friendly wrapper around /v1/chat/completions).

        Args:
            message: Your message
            model: Model key (e.g., "gpt-5"). Auto if None.
            system_prompt: System prompt
            history: Conversation history
            max_tokens: Max tokens
            temperature: Creativity (0.0-2.0)
            top_p: Nucleus sampling
            stream: Enable streaming (returns generator)

        Returns:
            ChatResponse or Generator[str]
        """
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")

        messages = _build_messages(message, system_prompt, history)
        return self.chat_completions(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream
        )

    def chat_completions(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        user: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Union[ChatResponse, Generator[str, None, None]]:
        """
        OpenAI-compatible chat completions endpoint.

        Args:
            messages: OpenAI-style messages list
            model: Model key. Auto if None.
            max_tokens: Max tokens
            temperature: Sampling temperature
            top_p: Nucleus sampling
            stop: Stop sequence(s)
            stream: Enable streaming
            user: End-user identifier
            response_format: e.g. {"type": "json_object"}

        Returns:
            ChatResponse or Generator[str]
        """
        if not messages:
            raise ValidationError("messages cannot be empty")

        payload: Dict[str, Any] = {
            "messages": messages,
            "stream": stream
        }
        if model:
            payload["model"] = model
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if stop:
            payload["stop"] = stop
        if user:
            payload["user"] = user
        if response_format:
            payload["response_format"] = response_format

        if stream:
            return self._stream_chat_completions(payload)

        response = self._request('POST', '/v1/chat/completions', json=payload)
        data = response.json()
        return self._parse_chat_completion(data)

    def _parse_chat_completion(self, data: Dict[str, Any]) -> ChatResponse:
        """Parse OpenAI-compatible chat completion response."""
        choice = data.get('choices', [{}])[0]
        message = choice.get('message', {})
        usage_data = data.get('usage', {})

        return ChatResponse(
            content=message.get('content', ''),
            reasoning_content=message.get('reasoning_content'),
            model=data.get('model', ''),
            model_id=data.get('model', ''),
            usage=UsageStats(
                prompt_tokens=usage_data.get('prompt_tokens', 0),
                completion_tokens=usage_data.get('completion_tokens', 0),
                total_tokens=usage_data.get('total_tokens', 0)
            ),
            finish_reason=choice.get('finish_reason', 'stop'),
            metadata={
                'id': data.get('id'),
                'created': data.get('created'),
                'object': data.get('object'),
                'system_fingerprint': data.get('system_fingerprint')
            }
        )

    def _stream_chat_completions(self, payload: Dict[str, Any]) -> Generator[str, None, None]:
        """Stream chat response using OpenAI SSE format."""
        response = self._request('POST', '/v1/chat/completions', json=payload, stream=True)

        for line in response.iter_lines():
            if not line:
                continue
            line_str = line.decode('utf-8')
            if not line_str.startswith('data: '):
                continue
            data_str = line_str[6:].strip()
            if data_str == '[DONE]':
                break
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            if 'error' in data:
                raise APIError(data['error'])

            for choice in data.get('choices', []):
                delta = choice.get('delta', {})
                content = delta.get('content')
                if content:
                    yield content

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        response = self._request('GET', '/api/v1/stats')
        return response.json()

    def list_models(self) -> List[ModelInfo]:
        """List available models from /v1/models"""
        response = self._request('GET', '/v1/models')
        data = response.json()
        models = []
        for item in data.get('data', []):
            models.append(ModelInfo(
                key=item.get('id', ''),
                name=item.get('id', ''),
                size='',
                owned_by=item.get('owned_by', ''),
                available_plans=[]
            ))
        return models

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

    BASE_URL = "https://api.sixfinger.live"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 120
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
            'User-Agent': 'sixfinger-python/2.1.1'
        }

    async def _get_session(self):
        """Lazy session initialization"""
        if self._session is None:
            try:
                import aiohttp
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                self._session = aiohttp.ClientSession(headers=self._headers, timeout=timeout)
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
            async with session.request(method, url, **kwargs) as response:
                if response.status == 401:
                    raise AuthenticationError(await _async_parse_error(response))
                elif response.status == 403:
                    raise AuthenticationError(await _async_parse_error(response))
                elif response.status == 429:
                    raise RateLimitError(await _async_parse_error(response))
                elif response.status >= 500:
                    raise APIError(f"Server error {response.status}: {await _async_parse_error(response)}")
                elif response.status >= 400:
                    raise ValidationError(await _async_parse_error(response))

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
        top_p: Optional[float] = None,
        stream: bool = False
    ) -> Union[ChatResponse, Generator[str, None, None]]:
        """Send chat message (async)"""
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")

        messages = _build_messages(message, system_prompt, history)
        return await self.chat_completions(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream
        )

    async def chat_completions(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        user: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        """OpenAI-compatible chat completions (async, non-streaming only)."""
        if not messages:
            raise ValidationError("messages cannot be empty")

        payload: Dict[str, Any] = {
            "messages": messages,
            "stream": stream
        }
        if model:
            payload["model"] = model
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if stop:
            payload["stop"] = stop
        if user:
            payload["user"] = user
        if response_format:
            payload["response_format"] = response_format

        if stream:
            raise NotImplementedError("Async streaming not yet implemented")

        data = await self._request('POST', '/v1/chat/completions', json=payload)
        return self._parse_chat_completion(data)

    def _parse_chat_completion(self, data: Dict[str, Any]) -> ChatResponse:
        """Parse OpenAI-compatible chat completion response."""
        choice = data.get('choices', [{}])[0]
        message = choice.get('message', {})
        usage_data = data.get('usage', {})

        return ChatResponse(
            content=message.get('content', ''),
            reasoning_content=message.get('reasoning_content'),
            model=data.get('model', ''),
            model_id=data.get('model', ''),
            usage=UsageStats(
                prompt_tokens=usage_data.get('prompt_tokens', 0),
                completion_tokens=usage_data.get('completion_tokens', 0),
                total_tokens=usage_data.get('total_tokens', 0)
            ),
            finish_reason=choice.get('finish_reason', 'stop'),
            metadata={
                'id': data.get('id'),
                'created': data.get('created'),
                'object': data.get('object'),
                'system_fingerprint': data.get('system_fingerprint')
            }
        )

    async def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics (async)"""
        return await self._request('GET', '/api/v1/stats')

    async def list_models(self) -> List[ModelInfo]:
        """List available models (async)"""
        data = await self._request('GET', '/v1/models')
        models = []
        for item in data.get('data', []):
            models.append(ModelInfo(
                key=item.get('id', ''),
                name=item.get('id', ''),
                size='',
                owned_by=item.get('owned_by', ''),
                available_plans=[]
            ))
        return models

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


async def _async_parse_error(response) -> str:
    """Extract error message from async OpenAI-compatible error response."""
    try:
        data = await response.json()
        if "error" in data:
            err = data["error"]
            if isinstance(err, dict):
                return err.get("message", str(err))
            return str(err)
        return await response.text() or f"HTTP {response.status}"
    except Exception:
        return await response.text() or f"HTTP {response.status}"


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
        return f"Conversation(messages={len(self.history)})"

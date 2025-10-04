from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import os
from dotenv import load_dotenv


class LLMProvider(str, Enum):
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


class BaseLLMClient(ABC):
    """Base class for LLM provider clients."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.

        Returns:
            {
                "text": str,
                "input_tokens": int,
                "output_tokens": int,
                "total_tokens": int
            }
        """
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        pass


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        from anthropic import Anthropic
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "text": response.content[0].text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # Claude 3.5 Sonnet pricing (as of 2024)
        return (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)


class GeminiClient(BaseLLMClient):
    """Google Gemini client."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        import google.generativeai as genai

        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        }

        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # Gemini token counting
        input_tokens = self.model.count_tokens(prompt).total_tokens
        output_tokens = self.model.count_tokens(response.text).total_tokens

        return {
            "text": response.text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # Gemini 2.0 Flash pricing (as of 2024)
        # Free tier: up to 1500 requests per day
        # Paid: $0.075 per 1M input tokens, $0.30 per 1M output tokens
        return (input_tokens * 0.075 / 1_000_000) + (output_tokens * 0.30 / 1_000_000)


class OpenRouterClient(BaseLLMClient):
    """OpenRouter client - supports ANY model!"""

    def __init__(self, api_key: Optional[str] = None, model: str = "google/gemini-2.5-flash"):
        import httpx

        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        import asyncio

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("SITE_URL", "https://github.com/ai-prompt-generator"),
            "X-Title": "AI Prompt Generator"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        # Retry logic for rate limits
        max_retries = 3
        base_delay = 2.0

        for attempt in range(max_retries):
            try:
                response = await self.client.post(
                    f"{self.base_url}/chat/completions",
                    json=data,
                    headers=headers,
                    timeout=30.0
                )

                # Check for HTTP errors
                if response.status_code != 200:
                    error_msg = f"HTTP {response.status_code}"
                    try:
                        error_body = response.json()
                        error_msg = f"{error_msg}: {error_body.get('error', {}).get('message', response.text)}"
                    except:
                        error_msg = f"{error_msg}: {response.text}"

                    # Check if it's a rate limit error
                    if response.status_code == 429 and attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"  ⏳ Rate limited, retrying in {delay}s...")
                        await asyncio.sleep(delay)
                        continue

                    raise Exception(f"OpenRouter API error: {error_msg}")

                result = response.json()

                # Extract response
                text = result["choices"][0]["message"]["content"]
                usage = result.get("usage", {})
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)

                return {
                    "text": text,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                }

            except Exception as e:
                if attempt < max_retries - 1 and "429" in str(e):
                    delay = base_delay * (2 ** attempt)
                    print(f"  ⏳ Rate limited, retrying in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    # Add debugging info
                    error_msg = f"OpenRouter API error: {str(e)}\nModel: {self.model}\nURL: {self.base_url}/chat/completions"
                    raise Exception(error_msg) from e

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # OpenRouter shows real-time pricing per model
        # Many models are FREE or very cheap!
        # For free models, return 0
        if ":free" in self.model:
            return 0.0

        # For paid models, estimate (varies by model)
        # Check https://openrouter.ai/models for exact pricing
        return (input_tokens * 0.0001 / 1000) + (output_tokens * 0.0002 / 1000)


def create_llm_client(
    provider: LLMProvider = LLMProvider.GEMINI,
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> BaseLLMClient:
    """
    Factory function to create LLM client.

    Args:
        provider: LLM provider to use
        api_key: Optional API key (otherwise from env)
        model: Optional model name

    Returns:
        LLM client instance
    """
    load_dotenv()

    if provider == LLMProvider.ANTHROPIC:
        default_model = "claude-3-5-sonnet-20241022"
        return AnthropicClient(api_key, model or default_model)
    elif provider == LLMProvider.GEMINI:
        default_model = "gemini-2.0-flash-exp"
        return GeminiClient(api_key, model or default_model)
    elif provider == LLMProvider.OPENROUTER:
        # Default to Gemini 2.5 Flash via OpenRouter
        default_model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
        return OpenRouterClient(api_key, model or default_model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

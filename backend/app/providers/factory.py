import logging
from typing import Optional
from app.config import settings
from app.providers.base import BaseLLMProvider
from app.providers.mock_provider import MockLLMProvider

logger = logging.getLogger(__name__)


def get_llm_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> BaseLLMProvider:
    """
    Returns the configured LLM provider.
    Gracefully falls back to MockLLMProvider if keys are missing,
    ensuring robust execution without crashes.
    """
    provider = (provider_name or settings.LLM_PROVIDER).lower()

    if provider == "openai":
        try:
            from app.providers.openai_provider import OpenAIProvider
            return OpenAIProvider(api_key=api_key, model=model)
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI provider ({e}). Falling back to MockLLMProvider.")
            return MockLLMProvider()

    elif provider in ("gemini", "google"):
        try:
            from app.providers.gemini_provider import GeminiProvider
            return GeminiProvider(api_key=api_key, model=model)
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini provider ({e}). Falling back to MockLLMProvider.")
            return MockLLMProvider()

    else:
        return MockLLMProvider()

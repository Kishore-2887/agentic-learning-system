import os
from fastapi import APIRouter
from app.config import settings
from app.schemas import SettingsResponse, SettingsUpdateRequest
from app.services.memory_service import memory_service

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("", response_model=SettingsResponse)
def get_settings():
    return SettingsResponse(
        llm_provider=settings.LLM_PROVIDER,
        available_providers=["mock", "openai", "google"],
        openai_model=settings.OPENAI_MODEL,
        gemini_model=settings.GEMINI_MODEL,
        default_quality_threshold=settings.DEFAULT_QUALITY_THRESHOLD,
        max_improvement_attempts=settings.MAX_IMPROVEMENT_ATTEMPTS,
        openai_key_configured=bool(settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")),
        gemini_key_configured=bool(settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")),
        persistent_memory_enabled=True,
        learned_rules=memory_service.get_learned_rules()
    )


@router.post("", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdateRequest):
    if payload.llm_provider:
        settings.LLM_PROVIDER = payload.llm_provider.lower()
    if payload.openai_model:
        settings.OPENAI_MODEL = payload.openai_model
    if payload.gemini_model:
        settings.GEMINI_MODEL = payload.gemini_model
    if payload.default_quality_threshold is not None:
        settings.DEFAULT_QUALITY_THRESHOLD = payload.default_quality_threshold
    if payload.max_improvement_attempts is not None:
        settings.MAX_IMPROVEMENT_ATTEMPTS = payload.max_improvement_attempts

    return get_settings()

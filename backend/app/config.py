from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    LLM_PROVIDER: str = Field(default="mock", description="mock, openai, or google")
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_MODEL: str = Field(default="gpt-4o")
    GEMINI_MODEL: str = Field(default="gemini-1.5-pro")

    DEFAULT_QUALITY_THRESHOLD: float = Field(default=80.0)
    MAX_IMPROVEMENT_ATTEMPTS: int = Field(default=3)

    DATABASE_URL: str = Field(default="sqlite:///./learning_agent.db")
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    ENVIRONMENT: str = Field(default="development")
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

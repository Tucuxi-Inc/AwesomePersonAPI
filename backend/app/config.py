"""Application configuration using Pydantic settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "AP API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://apapi:apapi_secret@localhost:5432/apapi"
    DATABASE_URL_SYNC: str = "postgresql://apapi:apapi_secret@localhost:5432/apapi"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 2 hours for development
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3003"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # LLM Provider Configuration
    ANTHROPIC_API_KEY: str = ""
    LLM_PROVIDER: str = "anthropic"  # anthropic, openai, google, groq, openrouter, ollama
    LLM_MODEL: str = ""  # Empty = use provider default
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://ollama:11434"

    # File Storage
    FILE_UPLOAD_DIR: str = "./uploads"
    MAX_RESUME_SIZE_MB: float = 10.0

    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@example.com"
    SMTP_FROM_NAME: str = "AP API Assessment"
    SMTP_USE_TLS: bool = True
    FRONTEND_BASE_URL: str = "http://localhost:3003"

    @property
    def smtp_configured(self) -> bool:
        """Check if SMTP is properly configured."""
        return bool(self.SMTP_USER and self.SMTP_PASSWORD)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

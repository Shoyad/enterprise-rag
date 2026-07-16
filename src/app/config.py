"""Typed application configuration, loaded from environment / .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://rag:rag@db:5432/rag"

    # Redis / background jobs
    redis_url: str = "redis://redis:6379/0"

    # Embeddings (local, keyless by default)
    embeddings_provider: str = "fastembed"
    embeddings_model: str = "BAAI/bge-small-en-v1.5"

    # Generation (real providers only; empty => answers disabled, not faked)
    generation_provider: str = ""
    generation_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Retrieval / chunking
    chunk_size_tokens: int = 512
    chunk_overlap_tokens: int = 64
    retrieval_top_k: int = 5

    # App
    log_level: str = "INFO"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()

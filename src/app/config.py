"""Typed application configuration, loaded from environment / .env.

Settings are added in the milestone that introduces the feature using them
(embeddings, chunking, generation, retrieval), to keep config honest about scope.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://rag:rag@db:5432/rag"
    redis_url: str = "redis://redis:6379/0"
    log_level: str = "INFO"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    # Actual implementation

    datalake_implementation: Optional[str] = None
    queue_implementation: Optional[str] = None

    aws_region: Optional[str] = None
    aws_bucket_name: Optional[str] = None
    sqs_queue_url: Optional[str] = None

    logfire_token: Optional[str] = None
    environment: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)


@lru_cache
def get_settings() -> Settings:
    return Settings()

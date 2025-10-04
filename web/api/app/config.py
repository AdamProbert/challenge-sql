from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="POKEDEX_")

    app_name: str = Field(default="Pokedex SQL Trainer API")
    api_version: str = Field(default="1.0.0")

    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="sqlchallenge")
    db_admin_user: str = Field(default="sqlchallenge")
    db_admin_password: str = Field(default="sqlchallenge")
    db_web_user: str = Field(default="sqlchallenge_web")
    db_web_password: str = Field(default="sqlchallenge_web")

    session_schema_prefix: str = Field(default="challenge_session_")
    session_ttl_minutes: int = Field(default=120)

    max_result_rows: int = Field(default=500)
    statement_timeout_ms: int = Field(default=5000)

    rate_limit_requests: int = Field(default=30, description="Allowed requests per window per session")
    rate_limit_window_seconds: int = Field(default=60)

    cors_allow_origins: list[str] = Field(default_factory=lambda: [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            import json

            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

@lru_cache
def get_settings() -> Settings:
    return Settings()

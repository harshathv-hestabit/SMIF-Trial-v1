from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

if not _ENV_PATH.exists():
    raise FileNotFoundError(
        f"[Settings] .env file not found at {_ENV_PATH}\n"
        f"  - In Docker: ensure the bind mount './.env:/app/.env:ro' is set in docker-compose.yaml\n"
        f"  - Locally: ensure .env exists at the project root"
    )


class Settings(BaseSettings):
    COSMOS_URL: str = Field(..., description="Cosmos DB endpoint")
    COSMOS_KEY: str = Field(..., description="Cosmos DB key")
    COSMOS_DB: str = Field(..., description="Cosmos DB name")
    CLIENT_PORTFOLIO_CONTAINER: str = Field(..., description="Client portfolio container")
    INSIGHTS_CONTAINER: str = Field(..., description="Insights container")

    model_config = SettingsConfigDict(
        env_file=_ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

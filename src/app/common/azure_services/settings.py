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


class AzureServiceEmulatorSettings(BaseSettings):
    COSMOS_URL: str = Field(..., description="Cosmos DB endpoint")
    COSMOS_KEY: str = Field(..., description="Cosmos DB key")
    COSMOS_DB: str = Field(..., description="Cosmos DB name")
    NEWS_CONTAINER: str = Field(..., description="News Container Name")
    CLIENT_PORTFOLIO_CONTAINER: str = Field(..., description="Client Portfolio Container Name")
    INSIGHTS_CONTAINER: str = Field(..., description="Insights Container Name")
    NEWS_CONTAINER_PARTITION_ID: str = Field(..., description="News Container Partition ID")
    CLIENT_PORTFOLIO_CONTAINER_PARTITION_ID: str = Field(
        ...,
        description="Client Portfolio Container Partition ID",
    )
    INSIGHTS_CONTAINER_PARTITION_ID: str = Field(..., description="Insights Container Partition ID")

    EVENTHUB_NAME: str = Field(..., description="Event Hub name")
    EVENTHUB_CONNECTION_STRING: str = Field(..., description="Event Hub Connection String")
    CHECKPOINT_CONTAINER: str = Field("eventhub-checkpoints", description="Event Hub checkpoint container")
    AZURE_STORAGE_ACCOUNT: str = Field(..., description="Storage account name")
    AZURE_STORAGE_KEY: str = Field(..., description="Storage account key")
    AZURE_STORAGE_CONNECTION_STRING: str = Field(..., description="Storage connection string")
    SERVICEBUS_CONNECTION_STRING: str = Field(..., description="Azure Service Bus connection string")
    QUEUE_REALTIME_NEWS: str = Field("realtime-news-events", description="Realtime workflow queue")
    QUEUE_DELAYED_NEWS: str = Field("delayed-news-events", description="Standard workflow queue")
    QUEUE_GENERATE_INSIGHT: str = Field("generate-insight-events", description="Generate insight queue")
    SERVICEBUS_MAX_DELIVERY_ATTEMPTS: int = Field(
        5,
        description="Dead-letter after this many delivery attempts",
    )

    model_config = SettingsConfigDict(
        env_file=_ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

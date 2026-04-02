from pydantic import Field

from app.common.azure_services.settings import AzureServiceEmulatorSettings


class Settings(AzureServiceEmulatorSettings):
    BACKUP_COPY_BATCH_SIZE: int = Field(
        200,
        description="Batch size used when reading Mongo backup documents for restore",
    )
    BACKUP_COPY_MONGO_SERVER_SELECTION_TIMEOUT_MS: int = Field(
        5000,
        description="MongoDB server selection timeout for backup restore startup",
    )


settings = Settings()

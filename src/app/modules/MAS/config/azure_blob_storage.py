from app.common.azure_services.eventhub import ensure_checkpoint_container as ensure_shared_checkpoint_container

from .settings import settings

async def ensure_checkpoint_container():
    await ensure_shared_checkpoint_container(
        settings.AZURE_STORAGE_CONNECTION_STRING,
        settings.CHECKPOINT_CONTAINER,
    )

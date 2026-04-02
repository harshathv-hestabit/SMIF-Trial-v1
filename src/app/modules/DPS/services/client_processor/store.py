from app.common.azure_services.cosmos import build_async_cosmos_client, ensure_async_container
from app.common.mongo_backup import backup_document_async
from app.modules.DPS.config.settings import settings


async def upsert_client_profiles(documents: list[dict]) -> None:
    async with build_async_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY) as client:
        container = await ensure_async_container(
            client,
            database_name=settings.COSMOS_DB,
            container_name=settings.CLIENT_PORTFOLIO_CONTAINER,
            partition_key_path=settings.CLIENT_PORTFOLIO_CONTAINER_PARTITION_ID,
        )

        for document in documents:
            await container.upsert_item(document)
            await backup_document_async(
                settings,
                collection_name=settings.CLIENT_PORTFOLIO_CONTAINER,
                document=document,
            )

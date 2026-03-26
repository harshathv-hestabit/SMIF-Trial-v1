from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient

from app.modules.DPS.config.settings import settings


async def upsert_client_profiles(documents: list[dict]) -> None:
    async with CosmosClient(
        settings.COSMOS_URL,
        credential=settings.COSMOS_KEY,
        connection_verify=False,
        enable_endpoint_discovery=False,
        connection_timeout=5,
    ) as client:
        db = await client.create_database_if_not_exists(settings.COSMOS_DB)
        try:
            container = await db.create_container_if_not_exists(
                id=settings.CLIENT_PORTFOLIO_CONTAINER,
                partition_key=PartitionKey(
                    path=settings.CLIENT_PORTFOLIO_CONTAINER_PARTITION_ID
                ),
            )
        except Exception:
            container = db.get_container_client(settings.CLIENT_PORTFOLIO_CONTAINER)

        for document in documents:
            await container.upsert_item(document)

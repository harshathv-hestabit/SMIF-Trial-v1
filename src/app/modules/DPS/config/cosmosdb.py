import asyncio

from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.core.exceptions import ServiceRequestError
from app.common.azure_services.cosmos import (
    build_async_cosmos_client,
    ensure_async_container,
    get_container_client,
    get_database_client,
)
from app.common.news_monitor import preserve_news_monitoring
from .settings import settings

_initialized = False
_async_client_instance = None

async def init_cosmos():
    global _initialized
    if _initialized:
        return

    client = build_async_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY)

    async with client:
        await ensure_async_container(
            client,
            database_name=settings.COSMOS_DB,
            container_name=settings.NEWS_CONTAINER,
            partition_key_path=settings.NEWS_CONTAINER_PARTITION_ID,
        )

    _initialized = True
    print("[Cosmos] Initialization complete")

class CosmosAsyncClient:
    def __init__(self):
        self.client = None
        self.database = None
        self.container = None

    async def connect(self):
        await init_cosmos()

        self.client = build_async_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY)
        self.database = get_database_client(self.client, settings.COSMOS_DB)
        self.container = get_container_client(self.database, settings.NEWS_CONTAINER)

    async def close(self):
        if self.client:
            await self.client.close()

    async def upsert_document(self, doc: dict):
        doc_id = doc.get("id")
        partition_key_field = settings.NEWS_CONTAINER_PARTITION_ID.lstrip("/")
        partition_key = doc.get(partition_key_field, doc_id)

        existing = None
        if doc_id is not None:
            try:
                existing = await self.container.read_item(doc_id, partition_key)
            except CosmosResourceNotFoundError:
                existing = None

        preserve_news_monitoring(doc, existing)
        await self.container.upsert_item(doc)
                
    async def read_document(self, doc_id, partition_key):
        return await self.container.read_item(doc_id, partition_key)

    def get_change_feed(self):
        return self.container.query_items_change_feed(
            is_start_from_beginning=False
        )

async def get_cosmos_async_client() -> CosmosAsyncClient:
    global _async_client_instance
    if _async_client_instance is None:
        client = CosmosAsyncClient()
        await client.connect()
        _async_client_instance = client

    return _async_client_instance

from __future__ import annotations

import logging
from typing import Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.common.azure_services.cosmos import (
    build_async_cosmos_client,
    ensure_async_container,
)
from app.modules.BACKUP_COPY.settings import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def _backup_enabled() -> bool:
    return bool(settings.MONGO_BACKUP_ENABLED and settings.MONGO_URI and settings.MONGO_DB)


def _container_specs() -> list[dict[str, str]]:
    return [
        {
            "name": settings.NEWS_CONTAINER,
            "partition_key_path": settings.NEWS_CONTAINER_PARTITION_ID,
        },
        {
            "name": settings.CLIENT_PORTFOLIO_CONTAINER,
            "partition_key_path": settings.CLIENT_PORTFOLIO_CONTAINER_PARTITION_ID,
        },
        {
            "name": settings.INSIGHTS_CONTAINER,
            "partition_key_path": settings.INSIGHTS_CONTAINER_PARTITION_ID,
        },
    ]


def _build_mongo_client() -> MongoClient:
    client = MongoClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=settings.BACKUP_COPY_MONGO_SERVER_SELECTION_TIMEOUT_MS,
    )
    client.admin.command("ping")
    return client


def _iter_backup_batches(
    mongo_client: MongoClient,
    *,
    collection_name: str,
    batch_size: int,
):
    collection = mongo_client[settings.MONGO_DB][collection_name]
    cursor = collection.find({}, no_cursor_timeout=False).batch_size(batch_size)
    try:
        batch: list[dict[str, Any]] = []
        for document in cursor:
            document.pop("_id", None)
            batch.append(document)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
    finally:
        cursor.close()


async def _restore_collection(
    cosmos_client,
    mongo_client: MongoClient,
    *,
    container_name: str,
    partition_key_path: str,
) -> int:
    container = await ensure_async_container(
        cosmos_client,
        database_name=settings.COSMOS_DB,
        container_name=container_name,
        partition_key_path=partition_key_path,
    )
    restored = 0
    found_any = False
    for batch in _iter_backup_batches(
        mongo_client,
        collection_name=container_name,
        batch_size=settings.BACKUP_COPY_BATCH_SIZE,
    ):
        found_any = True
        for document in batch:
            await container.upsert_item(document)
            restored += 1

    if not found_any:
        logger.info("backup_copy_collection_empty collection=%s", container_name)
        return 0

    logger.info(
        "backup_copy_collection_restored collection=%s documents=%s",
        container_name,
        restored,
    )
    return restored


async def main() -> int:
    if not _backup_enabled():
        logger.info("backup_copy_disabled reason=mongo_backup_not_configured")
        return 0

    total_restored = 0
    try:
        mongo_client = _build_mongo_client()
    except PyMongoError:
        logger.exception("backup_copy_mongo_connect_failed")
        return 1

    try:
        async with build_async_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY) as cosmos_client:
            for spec in _container_specs():
                total_restored += await _restore_collection(
                    cosmos_client,
                    mongo_client,
                    container_name=spec["name"],
                    partition_key_path=spec["partition_key_path"],
                )
    finally:
        mongo_client.close()

    logger.info("backup_copy_completed total_documents=%s", total_restored)
    return 0


if __name__ == "__main__":
    import asyncio
    import sys

    sys.exit(asyncio.run(main()))

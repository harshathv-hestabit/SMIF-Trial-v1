from __future__ import annotations

import asyncio
import logging
from copy import deepcopy
from threading import Lock
from typing import Any


logger = logging.getLogger(__name__)

_CLIENTS: dict[tuple[str, str], Any] = {}
_CLIENT_LOCK = Lock()


def _is_enabled(settings: Any) -> bool:
    return bool(
        getattr(settings, "MONGO_BACKUP_ENABLED", False)
        and getattr(settings, "MONGO_URI", "")
        and getattr(settings, "MONGO_DB", "")
    )


def _get_collection(settings: Any, collection_name: str):
    client_key = (settings.MONGO_URI, settings.MONGO_DB)

    with _CLIENT_LOCK:
        client = _CLIENTS.get(client_key)
        if client is None:
            from pymongo import MongoClient

            client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            _CLIENTS[client_key] = client

    return client[settings.MONGO_DB][collection_name]


def _normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(document)
    document_id = normalized.get("id")
    if document_id is None:
        raise ValueError("Mongo backup requires documents to include an 'id' field")
    normalized["_id"] = document_id
    return normalized


def backup_document_sync(
    settings: Any,
    *,
    collection_name: str,
    document: dict[str, Any],
) -> bool:
    if not _is_enabled(settings):
        return False

    try:
        normalized = _normalize_document(document)
        collection = _get_collection(settings, collection_name)
        collection.replace_one({"_id": normalized["_id"]}, normalized, upsert=True)
        return True
    except Exception:
        logger.exception("mongo_backup_sync_failed collection=%s", collection_name)
        return False


async def backup_document_async(
    settings: Any,
    *,
    collection_name: str,
    document: dict[str, Any],
) -> bool:
    return await asyncio.to_thread(
        backup_document_sync,
        settings,
        collection_name=collection_name,
        document=document,
    )

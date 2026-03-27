from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from azure.cosmos import CosmosClient
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient


TIMELINE_LIMIT = 50


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def update_news_lifecycle(
    document: dict[str, Any],
    *,
    stage: str,
    status: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    timestamp = utc_now_iso()
    monitoring = dict(document.get("monitoring") or {})
    stages = dict(monitoring.get("stages") or {})
    timeline = list(monitoring.get("timeline") or [])

    stage_record = dict(stages.get(stage) or {})
    stage_record.update(
        {
            "status": status,
            "timestamp": timestamp,
        }
    )
    if details:
        stage_record["details"] = details
    stages[stage] = stage_record

    event = {
        "stage": stage,
        "status": status,
        "timestamp": timestamp,
    }
    if details:
        event["details"] = details
    timeline.append(event)

    monitoring.update(
        {
            "current_stage": stage,
            "current_status": status,
            "updated_at": timestamp,
            "stages": stages,
            "timeline": timeline[-TIMELINE_LIMIT:],
        }
    )
    monitoring.setdefault("first_seen_at", timestamp)
    document["monitoring"] = monitoring
    return document


def preserve_news_monitoring(
    incoming: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    if existing is None:
        return incoming

    if "monitoring" in incoming:
        return incoming

    monitoring = existing.get("monitoring")
    if monitoring:
        incoming["monitoring"] = monitoring

    return incoming


def merge_news_monitoring(
    incoming: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    if existing is None:
        return incoming

    existing_monitoring = dict(existing.get("monitoring") or {})
    incoming_monitoring = dict(incoming.get("monitoring") or {})

    if not existing_monitoring:
        return incoming
    if not incoming_monitoring:
        incoming["monitoring"] = existing_monitoring
        return incoming

    merged_stages = dict(existing_monitoring.get("stages") or {})
    merged_stages.update(incoming_monitoring.get("stages") or {})

    merged_timeline = list(existing_monitoring.get("timeline") or [])
    seen_events = {
        (
            event.get("stage"),
            event.get("status"),
            event.get("timestamp"),
        )
        for event in merged_timeline
    }
    for event in incoming_monitoring.get("timeline") or []:
        event_key = (
            event.get("stage"),
            event.get("status"),
            event.get("timestamp"),
        )
        if event_key in seen_events:
            continue
        merged_timeline.append(event)
        seen_events.add(event_key)

    incoming["monitoring"] = {
        **existing_monitoring,
        **incoming_monitoring,
        "stages": merged_stages,
        "timeline": merged_timeline[-TIMELINE_LIMIT:],
        "first_seen_at": existing_monitoring.get("first_seen_at")
        or incoming_monitoring.get("first_seen_at")
        or utc_now_iso(),
    }
    return incoming


class SyncNewsMonitor:
    def __init__(
        self,
        *,
        cosmos_url: str,
        cosmos_key: str,
        cosmos_db: str,
        news_container: str,
    ) -> None:
        self._client = CosmosClient(
            cosmos_url,
            credential=cosmos_key,
            connection_verify=False,
            enable_endpoint_discovery=False,
            connection_timeout=5,
        )
        self._container = (
            self._client
            .get_database_client(cosmos_db)
            .get_container_client(news_container)
        )

    def close(self) -> None:
        close = getattr(self._client, "close", None)
        if callable(close):
            close()

    def record(
        self,
        *,
        news_id: str,
        partition_key: str | None = None,
        stage: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        document = self._container.read_item(
            item=news_id,
            partition_key=partition_key or news_id,
        )
        update_news_lifecycle(document, stage=stage, status=status, details=details)
        self._container.upsert_item(document)
        return document


class AsyncNewsMonitor:
    def __init__(
        self,
        *,
        cosmos_url: str,
        cosmos_key: str,
        cosmos_db: str,
        news_container: str,
    ) -> None:
        self._client = AsyncCosmosClient(
            cosmos_url,
            credential=cosmos_key,
            connection_verify=False,
            enable_endpoint_discovery=False,
            connection_timeout=5,
        )
        self._database = self._client.get_database_client(cosmos_db)
        self._container = self._database.get_container_client(news_container)

    async def close(self) -> None:
        close = getattr(self._client, "close", None)
        if callable(close):
            await close()

    async def record(
        self,
        *,
        news_id: str,
        partition_key: str | None = None,
        stage: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        document = await self._container.read_item(
            item=news_id,
            partition_key=partition_key or news_id,
        )
        update_news_lifecycle(document, stage=stage, status=status, details=details)
        await self._container.upsert_item(document)
        return document

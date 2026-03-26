import logging
import os
import sys
from pathlib import Path
from typing import Iterable

import azure.functions as func


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.common import ServiceBusPublisher, SyncNewsMonitor, build_event_payload  # noqa: E402


logger = logging.getLogger(__name__)


class QueuePublisher:
    def __init__(self) -> None:
        self._connection_string = os.environ["SERVICEBUS_CONNECTION_STRING"]
        self._queue_name = os.environ["QUEUE_REALTIME_NEWS"]
        self._monitor = SyncNewsMonitor(
            cosmos_url=os.environ["COSMOS_URL"],
            cosmos_key=os.environ["COSMOS_KEY"],
            cosmos_db=os.environ["COSMOS_DB"],
            news_container=os.environ["NEWS_CONTAINER"],
        )

    def close(self) -> None:
        self._monitor.close()

    def publish(self, news_id: str, partition_key: str | None = None) -> None:
        payload = build_event_payload(
            "realtime_news",
            {
                "news_doc_id": news_id,
                "partition_key": partition_key or news_id,
            },
            source="change_feed_service.cosmos_trigger",
            queue_name=self._queue_name,
        )

        with ServiceBusPublisher(self._connection_string) as publisher:
            publisher.publish_json(
                self._queue_name,
                payload,
                application_properties={
                    "event_type": payload["event_type"],
                    "source": payload["source"],
                },
                correlation_id=news_id,
                message_id=f"{payload['event_type']}-{news_id}",
                subject=payload["event_type"],
            )
        self._monitor.record(
            news_id=news_id,
            partition_key=partition_key,
            stage="change_feed_to_mas",
            status="queued",
            details={"queue_name": self._queue_name, "source": "change_feed_service"},
        )
        logger.info(
            "change_feed_servicebus_publish queue=%s news_doc_id=%s",
            self._queue_name,
            news_id,
        )


def _iter_news_ids(documents: Iterable[func.Document]) -> Iterable[tuple[str, str]]:
    for document in documents:
        item = document if isinstance(document, dict) else document.to_dict()
        news_id = item.get("id")
        if not news_id:
            logger.warning("change_feed_document_missing_id payload=%s", item)
            continue
        monitoring = item.get("monitoring") or {}
        stages = monitoring.get("stages") or {}
        if stages.get("change_feed_to_mas"):
            logger.info("change_feed_skip_already_queued news_doc_id=%s", news_id)
            continue

        yield news_id, item.get("id") or news_id


def main(documents: func.DocumentList) -> None:
    if not documents:
        logger.info("change_feed_trigger_received_empty_batch")
        return

    logger.info("change_feed_trigger_received batch_size=%s", len(documents))
    publisher = QueuePublisher()

    try:
        for news_id, partition_key in _iter_news_ids(documents):
            publisher.publish(news_id, partition_key=partition_key)
    finally:
        publisher.close()

import json
import logging
from typing import Any

from azure.eventhub import EventData

from app.common import update_news_lifecycle
from app.modules.DPS.config import EventConsumer, get_cosmos_async_client
from .transform import normalize_news_document


logger = logging.getLogger(__name__)


class NewsProcessorService:
    def __init__(self) -> None:
        self.cosmos = None
        self.consumer = EventConsumer(consumer_group="DPS")

    async def start(self) -> None:
        self.cosmos = await get_cosmos_async_client()
        logger.info("news_processor_starting")

        try:
            async with self.consumer:
                logger.info(
                    "news_processor_listening eventhub=%s consumer_group=%s",
                    self.consumer.hub,
                    self.consumer.consumer_group,
                )
                await self.consumer.receive(self._on_event)
        finally:
            if self.cosmos is not None:
                await self.cosmos.close()

    async def _on_event(self, partition_context: Any, event: EventData) -> None:
        article_id = "unknown"
        try:
            payload = json.loads(event.body_as_str(encoding="UTF-8"))
            normalized = normalize_news_document(payload)
            article_id = normalized["id"]
            update_news_lifecycle(
                normalized,
                stage="dps_news_processor",
                status="stored",
                details={
                    "partition_id": str(partition_context.partition_id),
                    "sequence_number": int(event.sequence_number),
                    "source": "eventhub",
                },
            )
            update_news_lifecycle(
                normalized,
                stage="retail_batch",
                status="pending",
                details={"target_workflow": "standard"},
            )
            await self.cosmos.upsert_document(normalized)
            await partition_context.update_checkpoint(event)
            logger.info(
                "news_processor_upsert_ok partition_id=%s sequence_number=%s article_id=%s",
                partition_context.partition_id,
                event.sequence_number,
                article_id,
            )
        except Exception:
            logger.exception(
                "news_processor_upsert_failed partition_id=%s sequence_number=%s article_id=%s",
                partition_context.partition_id,
                event.sequence_number,
                article_id,
            )

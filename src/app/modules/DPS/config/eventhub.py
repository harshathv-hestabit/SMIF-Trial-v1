import json
import logging

from azure.eventhub import EventData
from app.common.azure_services.eventhub import (
    build_checkpoint_store,
    build_eventhub_consumer,
    build_eventhub_producer,
    ensure_checkpoint_container as ensure_shared_checkpoint_container,
)

from .settings import settings


logger = logging.getLogger(__name__)
logging.getLogger("azure.eventhub").setLevel(logging.WARNING)


async def ensure_checkpoint_container() -> None:
    await ensure_shared_checkpoint_container(
        settings.AZURE_STORAGE_CONNECTION_STRING,
        settings.CHECKPOINT_CONTAINER,
    )

class EventProducer:
    def __init__(self):        
        self.producer = build_eventhub_producer(
            settings.EVENTHUB_CONNECTION_STRING,
            settings.EVENTHUB_NAME,
        )

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.producer.close()
        return False
    
    async def publish(self, news_id: str, partition_key: str | None = None):
        logger.info("realtime_eventhub_publish news_doc_id=%s", news_id)
        payload = json.dumps({
            "event_type": "realtime_news",
            "news_doc_id": news_id,
            "partition_key": partition_key or news_id,
        }).encode("utf-8")

        event = EventData(payload)
        event.properties = {
            "event_type": "realtime_news"
        }
        await self.producer.send_event(event)


class EventConsumer:
    def __init__(self, consumer_group: str = "DPS"):
        self.conn = settings.EVENTHUB_CONNECTION_STRING
        self.hub = settings.EVENTHUB_NAME
        self.consumer_group = consumer_group
        self.consumer = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
        return False

    async def start(self) -> None:
        if self.consumer is not None:
            return

        await ensure_checkpoint_container()
        checkpoint_store = build_checkpoint_store(
            settings.AZURE_STORAGE_CONNECTION_STRING,
            settings.CHECKPOINT_CONTAINER,
        )
        self.consumer = build_eventhub_consumer(
            self.conn,
            self.hub,
            self.consumer_group,
            checkpoint_store=checkpoint_store,
        )

    async def receive(self, on_event) -> None:
        if self.consumer is None:
            await self.start()

        await self.consumer.receive(
            on_event=on_event,
            starting_position="-1",
        )

    async def close(self) -> None:
        if self.consumer is None:
            return

        await self.consumer.close()
        self.consumer = None

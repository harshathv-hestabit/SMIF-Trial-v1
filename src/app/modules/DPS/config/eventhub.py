import json
import logging

from azure.core.exceptions import ResourceExistsError
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient, EventHubProducerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.storage.blob.aio import BlobServiceClient

from .settings import settings


logger = logging.getLogger(__name__)
logging.getLogger("azure.eventhub").setLevel(logging.WARNING)


async def ensure_checkpoint_container() -> None:
    async with BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING) as client:
        container = client.get_container_client(settings.CHECKPOINT_CONTAINER)
        try:
            await container.create_container()
            logger.info("eventhub_checkpoint_container_created container=%s", settings.CHECKPOINT_CONTAINER)
        except ResourceExistsError:
            logger.info("eventhub_checkpoint_container_ready container=%s", settings.CHECKPOINT_CONTAINER)

class EventProducer:
    def __init__(self):        
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=settings.EVENTHUB_CONNECTION_STRING,
            eventhub_name=settings.EVENTHUB_NAME
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
        checkpoint_store = BlobCheckpointStore.from_connection_string(
            conn_str=settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=settings.CHECKPOINT_CONTAINER,
        )
        self.consumer = EventHubConsumerClient.from_connection_string(
            conn_str=self.conn,
            eventhub_name=self.hub,
            consumer_group=self.consumer_group,
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

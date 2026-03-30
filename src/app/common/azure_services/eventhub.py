import logging

from azure.core.exceptions import ResourceExistsError
from azure.eventhub.aio import EventHubConsumerClient, EventHubProducerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.storage.blob.aio import BlobServiceClient


logger = logging.getLogger(__name__)


async def ensure_checkpoint_container(
    storage_connection_string: str,
    checkpoint_container: str,
) -> None:
    async with BlobServiceClient.from_connection_string(storage_connection_string) as client:
        container = client.get_container_client(checkpoint_container)
        try:
            await container.create_container()
            logger.info("eventhub_checkpoint_container_created container=%s", checkpoint_container)
        except ResourceExistsError:
            logger.info("eventhub_checkpoint_container_ready container=%s", checkpoint_container)


def build_checkpoint_store(
    storage_connection_string: str,
    checkpoint_container: str,
) -> BlobCheckpointStore:
    return BlobCheckpointStore.from_connection_string(
        conn_str=storage_connection_string,
        container_name=checkpoint_container,
    )


def build_eventhub_consumer(
    eventhub_connection_string: str,
    eventhub_name: str,
    consumer_group: str,
    checkpoint_store: BlobCheckpointStore | None = None,
) -> EventHubConsumerClient:
    return EventHubConsumerClient.from_connection_string(
        conn_str=eventhub_connection_string,
        eventhub_name=eventhub_name,
        consumer_group=consumer_group,
        checkpoint_store=checkpoint_store,
    )


def build_eventhub_producer(
    eventhub_connection_string: str,
    eventhub_name: str,
) -> EventHubProducerClient:
    return EventHubProducerClient.from_connection_string(
        conn_str=eventhub_connection_string,
        eventhub_name=eventhub_name,
    )

import json
import logging

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

from .settings import settings


logger = logging.getLogger(__name__)
logging.getLogger("azure.eventhub").setLevel(logging.WARNING)

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

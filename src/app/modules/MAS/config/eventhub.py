from app.common.azure_services.eventhub import build_checkpoint_store, build_eventhub_consumer

from .settings import settings

class EventConsumer:
    def __init__(self):
        self.conn = settings.EVENTHUB_CONNECTION_STRING
        self.hub = settings.EVENTHUB_NAME
        self.consumer_group = "MAS"
        self.checkpoint_store = build_checkpoint_store(
            settings.AZURE_STORAGE_CONNECTION_STRING,
            settings.CHECKPOINT_CONTAINER,
        )
        self.consumer = build_eventhub_consumer(
            self.conn,
            self.hub,
            self.consumer_group,
            checkpoint_store=self.checkpoint_store,
        )

    def client(self):
        return self.consumer

import os
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

class EventConsumer:
    def __init__(self):
        self.conn = (
            "Endpoint=sb://localhost;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=SAS_KEY_VALUE;"
            "UseDevelopmentEmulator=true;"
        )

        self.hub = os.getenv("EVENTHUB_NAME")
        self.consumer_group = "MAS"

        blob_conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        self.checkpoint_store = BlobCheckpointStore.from_connection_string(
            conn_str=blob_conn,
            container_name="eventhub-checkpoints"
        )

        self.consumer = EventHubConsumerClient.from_connection_string(
            conn_str=self.conn,
            eventhub_name=self.hub,
            consumer_group=self.consumer_group,
            checkpoint_store=self.checkpoint_store
        )


    def client(self):
        return self.consumer
import asyncio
import json
import logging
from typing import Any

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub.exceptions import EventHubError

logger = logging.getLogger(__name__)


class EventHubPublisher:
    def __init__(self, connection_string: str, eventhub_name: str) -> None:
        self._connection_string = connection_string
        self._eventhub_name = eventhub_name
        self._producer: EventHubProducerClient | None = None
        self._is_ready = False

    @property
    def is_ready(self) -> bool:
        return self._is_ready and self._producer is not None

    async def start(self) -> None:
        if self._producer is not None:
            return

        self._producer = EventHubProducerClient.from_connection_string(
            conn_str=self._connection_string,
            eventhub_name=self._eventhub_name,
        )

        try:
            self._is_ready = True
            logger.info("eventhub_producer_ready eventhub=%s", self._eventhub_name)
        except Exception:
            await self._producer.close()
            self._producer = None
            self._is_ready = False
            logger.exception("eventhub_producer_init_failed eventhub=%s", self._eventhub_name)
            raise
        
    async def publish(
        self,
        payload: dict[str, Any],
        properties: dict[str, str] | None = None,
        max_retries: int = 3,
    ) -> None:
        if self._producer is None:
            raise RuntimeError("Event Hub producer not initialized")

        message = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            try:
                event = EventData(message)
                if properties:
                    event.properties = properties
                await self._producer.send_event(event)
                print("EVENT PUBLISHED")
                return
            except EventHubError as exc:
                last_error = exc
                print("EVENTHUB ERROR!!!: ",exc)
                if attempt == max_retries:
                    break
                backoff_seconds = min(2 ** (attempt - 1), 8)
                logger.warning(
                    "eventhub_publish_retry attempt=%s/%s backoff_seconds=%s error=%s",
                    attempt,
                    max_retries,
                    backoff_seconds,
                    type(exc).__name__,
                )
                await asyncio.sleep(backoff_seconds)

        raise RuntimeError("Failed to publish event to Event Hub") from last_error

    async def close(self) -> None:
        if self._producer is None:
            self._is_ready = False
            return

        await self._producer.close()
        self._producer = None
        self._is_ready = False
        logger.info("eventhub_producer_closed")

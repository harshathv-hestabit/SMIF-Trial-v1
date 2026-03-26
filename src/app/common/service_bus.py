import json
import logging
from datetime import datetime, timezone
from typing import Any

from azure.servicebus import ServiceBusClient as SyncServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.servicebus import ServiceBusReceiveMode
from azure.servicebus.aio import ServiceBusClient as AsyncServiceBusClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logging.getLogger("azure.servicebus").setLevel(logging.WARNING)
logging.getLogger("uamqp").setLevel(logging.WARNING)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_event_payload(
    event_type: str,
    payload: dict[str, Any],
    *,
    source: str,
    queue_name: str,
) -> dict[str, Any]:
    message = dict(payload)
    message.setdefault("event_type", event_type)
    message.setdefault("created_at", utc_now_iso())
    message.setdefault("source", source)
    message.setdefault("queue_name", queue_name)
    return message


def _to_service_bus_message(
    payload: dict[str, Any],
    *,
    application_properties: dict[str, Any] | None = None,
    message_id: str | None = None,
    correlation_id: str | None = None,
    subject: str | None = None,
    scheduled_enqueue_time_utc: datetime | None = None,
) -> ServiceBusMessage:
    return ServiceBusMessage(
        json.dumps(payload),
        application_properties=application_properties or {},
        message_id=message_id,
        correlation_id=correlation_id,
        subject=subject,
        scheduled_enqueue_time_utc=scheduled_enqueue_time_utc,
    )


def decode_message_body(message: Any) -> dict[str, Any]:
    body = b"".join(bytes(chunk) for chunk in message.body)
    if not body:
        return {}
    return json.loads(body.decode("utf-8"))


class ServiceBusPublisher:
    def __init__(self, connection_string: str):
        if not connection_string:
            raise ValueError("SERVICEBUS_CONNECTION_STRING is required")
        self._client = SyncServiceBusClient.from_connection_string(
            conn_str=connection_string
        )

    def __enter__(self) -> "ServiceBusPublisher":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False

    def close(self) -> None:
        self._client.close()

    def publish_json(
        self,
        queue_name: str,
        payload: dict[str, Any],
        *,
        application_properties: dict[str, Any] | None = None,
        message_id: str | None = None,
        correlation_id: str | None = None,
        subject: str | None = None,
        scheduled_enqueue_time_utc: datetime | None = None,
    ) -> None:
        message = _to_service_bus_message(
            payload,
            application_properties=application_properties,
            message_id=message_id,
            correlation_id=correlation_id,
            subject=subject,
            scheduled_enqueue_time_utc=scheduled_enqueue_time_utc,
        )
        with self._client.get_queue_sender(queue_name=queue_name) as sender:
            sender.send_messages(message)


class AsyncServiceBusPublisher:
    def __init__(self, connection_string: str):
        if not connection_string:
            raise ValueError("SERVICEBUS_CONNECTION_STRING is required")
        self._client = AsyncServiceBusClient.from_connection_string(
            conn_str=connection_string
        )

    async def __aenter__(self) -> "AsyncServiceBusPublisher":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        await self.close()
        return False

    async def close(self) -> None:
        await self._client.close()

    async def publish_json(
        self,
        queue_name: str,
        payload: dict[str, Any],
        *,
        application_properties: dict[str, Any] | None = None,
        message_id: str | None = None,
        correlation_id: str | None = None,
        subject: str | None = None,
        scheduled_enqueue_time_utc: datetime | None = None,
    ) -> None:
        message = _to_service_bus_message(
            payload,
            application_properties=application_properties,
            message_id=message_id,
            correlation_id=correlation_id,
            subject=subject,
            scheduled_enqueue_time_utc=scheduled_enqueue_time_utc,
        )
        async with self._client.get_queue_sender(queue_name=queue_name) as sender:
            await sender.send_messages(message)

    def get_queue_receiver(
        self,
        queue_name: str,
        *,
        prefetch_count: int = 0,
        max_wait_time: int = 5,
    ):
        return self._client.get_queue_receiver(
            queue_name=queue_name,
            prefetch_count=prefetch_count,
            receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
            max_wait_time=max_wait_time,
        )

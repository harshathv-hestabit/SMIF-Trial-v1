__all__ = (
    "get_cosmos_async_client",
    "EventConsumer",
    "EventProducer",
    "AsyncServiceBusPublisher",
    "ServiceBusPublisher",
    "build_event_payload",
    "decode_message_body",
)


def __getattr__(name: str):
    if name == "get_cosmos_async_client":
        from .cosmosdb import get_cosmos_async_client

        return get_cosmos_async_client
    if name in {"EventConsumer", "EventProducer"}:
        from .eventhub import EventConsumer, EventProducer

        return {"EventConsumer": EventConsumer, "EventProducer": EventProducer}[name]
    if name in {
        "AsyncServiceBusPublisher",
        "ServiceBusPublisher",
        "build_event_payload",
        "decode_message_body",
    }:
        from .service_bus import (
            AsyncServiceBusPublisher,
            ServiceBusPublisher,
            build_event_payload,
            decode_message_body,
        )

        return {
            "AsyncServiceBusPublisher": AsyncServiceBusPublisher,
            "ServiceBusPublisher": ServiceBusPublisher,
            "build_event_payload": build_event_payload,
            "decode_message_body": decode_message_body,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

from ..config import ServiceBusPublisher, build_event_payload, settings


class EventExecutor:
    def __init__(self):
        self.publisher = ServiceBusPublisher(settings.SERVICEBUS_CONNECTION_STRING)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.publisher.close()
        return False

    def publish_insight_events(self, insight_events: list[dict]) -> None:
        for event_payload in insight_events:
            payload = build_event_payload(
                "generate_insight",
                event_payload,
                source=event_payload.get("source", "mas.workflow"),
                queue_name=settings.QUEUE_GENERATE_INSIGHT,
            )
            self.publisher.publish_json(
                settings.QUEUE_GENERATE_INSIGHT,
                payload,
                application_properties={
                    "event_type": "generate_insight",
                    "client_id": event_payload["client_id"],
                    "news_doc_id": event_payload.get("news_doc_id", ""),
                    "source": payload["source"],
                },
                correlation_id=event_payload["client_id"],
                message_id=(
                    f"insight-{event_payload['client_id']}-"
                    f"{event_payload.get('news_doc_id', 'unknown')}"
                ),
                subject="generate_insight",
            )

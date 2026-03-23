import logging

from ..config import AsyncServiceBusPublisher, build_event_payload
from ..config.settings import settings


logger = logging.getLogger(__name__)


async def publish_standard_news_event(
    checkpoint_start: str,
    checkpoint_end: str,
    *,
    job_id: str,
    source: str = "dps.scheduler",
) -> None:
    payload = build_event_payload(
        "standard_news",
        {
            "job_id": job_id,
            "checkpoint_start": checkpoint_start,
            "checkpoint_end": checkpoint_end,
        },
        source=source,
        queue_name=settings.QUEUE_STANDARD_NEWS,
    )
    logger.info(
        "standard_dispatch_publish queue=%s job_id=%s checkpoint_start=%s checkpoint_end=%s",
        settings.QUEUE_STANDARD_NEWS,
        job_id,
        checkpoint_start,
        checkpoint_end,
    )

    async with AsyncServiceBusPublisher(settings.SERVICEBUS_CONNECTION_STRING) as publisher:
        await publisher.publish_json(
            settings.QUEUE_STANDARD_NEWS,
            payload,
            application_properties={
                "event_type": payload["event_type"],
                "source": payload["source"],
            },
            correlation_id=job_id,
            message_id=f"standard-{job_id}",
            subject="standard_news",
        )

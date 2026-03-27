import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import azure.functions as func


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.common import ServiceBusPublisher, build_event_payload  # noqa: E402


logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _delay_minutes() -> int:
    raw_value = os.getenv("STANDARD_TRIGGER_DELAY_MINUTES", "2")
    try:
        delay = int(raw_value)
    except ValueError as exc:
        raise RuntimeError("STANDARD_TRIGGER_DELAY_MINUTES must be an integer") from exc

    if delay < 0:
        raise RuntimeError("STANDARD_TRIGGER_DELAY_MINUTES must be >= 0")

    return delay


def _build_payload(
    job_id: str,
    *,
    requested_at: datetime,
    enqueue_at: datetime,
    delay_minutes: int,
) -> dict:
    queue_name = _require_env("QUEUE_DELAYED_NEWS")
    return build_event_payload(
        "standard_news",
        {
            "job_id": job_id,
            "trigger_type": "timer",
            "requested_at": requested_at.isoformat(),
            "checkpoint_end": requested_at.isoformat(),
            "scheduled_enqueue_time_utc": enqueue_at.isoformat(),
            "delay_minutes": delay_minutes,
        },
        source="functions.standard_trigger",
        queue_name=queue_name,
    )


def main(mytimer: func.TimerRequest) -> None:
    now = _utc_now()
    delay_minutes = _delay_minutes()
    enqueue_at = now + timedelta(minutes=delay_minutes)
    job_id = f"standard-{now.strftime('%Y%m%d%H%M%S')}"
    queue_name = _require_env("QUEUE_DELAYED_NEWS")
    connection_string = _require_env("SERVICEBUS_CONNECTION_STRING")

    payload = _build_payload(
        job_id,
        requested_at=now,
        enqueue_at=enqueue_at,
        delay_minutes=delay_minutes,
    )

    if mytimer.past_due:
        logger.warning("standard_trigger_past_due job_id=%s", job_id)

    with ServiceBusPublisher(connection_string) as publisher:
        publisher.publish_json(
            queue_name,
            payload,
            application_properties={
                "event_type": payload["event_type"],
                "source": payload["source"],
            },
            correlation_id=job_id,
            message_id=job_id,
            subject=payload["event_type"],
            scheduled_enqueue_time_utc=enqueue_at,
        )

    logger.info(
        "standard_trigger_scheduled queue=%s job_id=%s enqueue_at=%s delay_minutes=%s",
        queue_name,
        job_id,
        enqueue_at.isoformat(),
        delay_minutes,
    )

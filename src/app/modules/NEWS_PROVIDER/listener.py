import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import websockets

from app.common.settings import settings
from .publisher import EventHubPublisher

logger = logging.getLogger(__name__)


@dataclass
class ListenerStats:
    messages_received: int = 0
    messages_published: int = 0
    reconnect_count: int = 0
    last_event_time: str | None = None
    websocket_connected: bool = False
    invalid_json_count: int = 0
    publish_error_count: int = 0


@dataclass
class NewsStreamListener:
    publisher: EventHubPublisher
    benzinga_api_key: str
    stats: ListenerStats = field(default_factory=ListenerStats)
    _stop_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)

    @property
    def ws_url(self) -> str:
        return f"wss://api.benzinga.com/api/v1/news/stream?token={self.benzinga_api_key}"

    def stop(self) -> None:
        self._stop_event.set()

    async def run_forever(self) -> None:
        backoff_seconds = 1

        while not self._stop_event.is_set():
            try:
                await self._run_connection()
                backoff_seconds = 1
            except asyncio.CancelledError:
                self.stats.websocket_connected = False
                raise
            except Exception as exc:
                self.stats.websocket_connected = False
                self.stats.reconnect_count += 1
                logger.warning(
                    "ws_disconnected reconnect_count=%s backoff_seconds=%s error=%s",
                    self.stats.reconnect_count,
                    backoff_seconds,
                    type(exc).__name__,
                )
                await asyncio.sleep(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, 30)

        self.stats.websocket_connected = False

    async def _run_connection(self) -> None:
        async with websockets.connect(
            self.ws_url,
            ping_interval=20,
            ping_timeout=20,
            close_timeout=10,
        ) as ws:
            self.stats.websocket_connected = True
            logger.info("ws_connected")

            while not self._stop_event.is_set():
                raw_message = await ws.recv()
                await self._process_message(raw_message)

    async def _process_message(self, raw_message: str | bytes) -> None:
        if isinstance(raw_message, bytes):
            raw_message = raw_message.decode("utf-8", errors="ignore")

        try:
            payload = json.loads(raw_message)
        except json.JSONDecodeError:
            self.stats.invalid_json_count += 1
            logger.warning("ws_invalid_json")
            return

        if not isinstance(payload, dict):
            logger.warning("ws_non_object_payload payload_type=%s", type(payload).__name__)
            return

        ingested_at = datetime.now(timezone.utc).isoformat()

        enriched_payload: dict[str, Any] = {
            **payload,
            "event_type": "news_stream",
            "source": "benzinga_ws",
            "ingested_at": ingested_at,
            "trace_id": str(uuid4()),
        }

        self.stats.messages_received += 1
        self.stats.last_event_time = ingested_at

        try:
            await self.publisher.publish(
                enriched_payload,
                properties={"event_type": "news_stream"},
            )
            self.stats.messages_published += 1
        except Exception:
            self.stats.publish_error_count += 1
            logger.exception("event_publish_failed")


async def create_listener(publisher: EventHubPublisher) -> NewsStreamListener:
    return NewsStreamListener(
        publisher=publisher,
        benzinga_api_key=settings.BENZINGA_API_KEY,
    )

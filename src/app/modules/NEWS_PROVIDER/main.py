import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.common.settings import settings
from .listener import NewsStreamListener, create_listener
from .publisher import EventHubPublisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("uamqp").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class ServiceContainer:
    def __init__(self) -> None:
        self.publisher = EventHubPublisher(
            connection_string=settings.EVENTHUB_CONNECTION_STRING,
            eventhub_name=settings.EVENTHUB_NAME,
        )
        self.listener: NewsStreamListener | None = None
        self.listener_task: asyncio.Task | None = None


container = ServiceContainer()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("news_provider_starting")

    await container.publisher.start()
    container.listener = await create_listener(container.publisher)
    container.listener_task = asyncio.create_task(container.listener.run_forever())

    try:
        yield
    finally:
        logger.info("news_provider_stopping")

        if container.listener is not None:
            container.listener.stop()

        if container.listener_task is not None:
            container.listener_task.cancel()
            try:
                await container.listener_task
            except asyncio.CancelledError:
                pass

        await container.publisher.close()


app = FastAPI(title="news-provider-service", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/ready")
async def ready() -> JSONResponse:
    listener = container.listener
    is_ws_connected = bool(listener and listener.stats.websocket_connected)
    is_producer_ready = container.publisher.is_ready
    is_ready = is_ws_connected and is_producer_ready

    payload = {
        "ready": is_ready,
        "websocket_connected": is_ws_connected,
        "producer_ready": is_producer_ready,
    }
    status_code = 200 if is_ready else 503
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/stats")
async def stats() -> dict[str, Any]:
    listener = container.listener
    if listener is None:
        return {
            "messages_received": 0,
            "messages_published": 0,
            "reconnect_count": 0,
            "last_event_time": None,
        }

    return {
        "messages_received": listener.stats.messages_received,
        "messages_published": listener.stats.messages_published,
        "reconnect_count": listener.stats.reconnect_count,
        "last_event_time": listener.stats.last_event_time,
    }

import asyncio
import logging

from .service import NewsProcessorService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("uamqp").setLevel(logging.WARNING)


async def _main() -> None:
    service = NewsProcessorService()
    await service.start()


if __name__ == "__main__":
    asyncio.run(_main())

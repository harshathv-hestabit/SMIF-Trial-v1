import uvicorn

from .settings import settings


if __name__ == "__main__":
    uvicorn.run(
        "app.modules.UI_API.main:app",
        host=settings.HOST_URL,
        port=settings.UI_API_PORT,
        log_level="info",
    )

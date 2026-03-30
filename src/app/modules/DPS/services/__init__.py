__all__ = ("ChangeFeedListener", "ClientProcessorService")


def __getattr__(name: str):
    if name == "ChangeFeedListener":
        from .change_feed_service import ChangeFeedListener

        return ChangeFeedListener
    if name == "ClientProcessorService":
        from .client_processor import ClientProcessorService

        return ClientProcessorService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

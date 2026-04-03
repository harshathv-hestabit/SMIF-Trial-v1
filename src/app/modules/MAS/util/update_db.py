from datetime import datetime
from app.common.azure_services.cosmos import build_async_cosmos_client, ensure_async_container
from app.common.mongo_backup import backup_document_async
from ..config import settings


def build_insight_document_id(client_id: str, news_doc_id: str | None) -> str:
    return f"insight:{client_id}:{news_doc_id or 'unknown'}"


async def update_db(state: dict):
    async with build_async_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY) as client:
        container = await ensure_async_container(
            client,
            database_name=settings.COSMOS_DB,
            container_name=settings.INSIGHTS_CONTAINER,
            partition_key_path=settings.INSIGHTS_CONTAINER_PARTITION_ID,
        )
        news = state["news_document"]
        client_id = state["client_id"]
        news_doc_id = news.get("id")
        doc = {
            "id": build_insight_document_id(client_id, news_doc_id),
            "type": "insight",
            "workflow_type": "generate_insight",
            "job_key": state.get("job_key"),
            "client_id": client_id,
            "news_doc_id": news_doc_id,
            "insight": state["insight_draft"],
            "verification_score": state["verification_score"],
            "news_title": news.get("title"),
            "tickers": state.get("matched_tickers") or news.get("tickers") or news.get("symbols"),
            "matched_holdings": state.get("matched_holdings", []),
            "relevance": state.get("relevance", {}),
            "portfolio_snapshot": state.get("portfolio_snapshot", {}),
            "client_profile_summary": state.get("client_profile_summary", {}),
            "status": state["status"],
            "token_usage": state.get("token_usage", {}),
            "timestamp": datetime.now().isoformat(),
        }

        await container.upsert_item(doc)
        await backup_document_async(
            settings,
            collection_name=settings.INSIGHTS_CONTAINER,
            document=doc,
        )

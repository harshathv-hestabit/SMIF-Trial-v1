from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from azure.cosmos import CosmosClient
from app.common import merge_news_monitoring, update_news_lifecycle
from ..config import process_news_stream, settings
from ..util import EventExecutor

cosmos_client = CosmosClient(
    url=settings.COSMOS_URL,
    credential=settings.COSMOS_KEY,
    connection_verify=False,
    enable_endpoint_discovery=False,
    connection_timeout=5,
)

news_container = (
    cosmos_client
    .get_database_client(settings.COSMOS_DB)
    .get_container_client(settings.NEWS_CONTAINER)
)

class HNWState(TypedDict):
    event_data: dict
    news_doc: Optional[dict]
    relevance_results: dict[str, list[dict]]
    candidate_clients: list[dict]
    generate_insight_events: list[dict]

RELEVANCE_THRESHOLD = 0.8

def hnw_agent_activation(state: HNWState) -> HNWState:
    print(f"[HNW] Activated with event: {state['event_data']}")
    return state


def _record_news_stage(
    news_doc: dict,
    *,
    stage: str,
    status: str,
    details: dict | None = None,
) -> None:
    latest_doc = news_container.read_item(
        item=news_doc["id"],
        partition_key=news_doc.get("id"),
    )
    merge_news_monitoring(news_doc, latest_doc)
    update_news_lifecycle(news_doc, stage=stage, status=status, details=details)
    news_container.upsert_item(news_doc)


def fetch_news_document(state: HNWState) -> HNWState:
    news_doc_id = state["event_data"]["news_doc_id"]
    partition_key = state["event_data"].get("partition_key", news_doc_id)
    doc = news_container.read_item(item=news_doc_id, partition_key=partition_key)
    state["news_doc"] = doc
    _record_news_stage(
        doc,
        stage="mas_hnw",
        status="processing",
        details={"source_queue": state["event_data"].get("queue_name", "unknown")},
    )

    print(f"[HNW] Fetched news doc '{news_doc_id}': {doc.get('title', '')[:60]}")
    return state

def score_relevance(state: HNWState) -> HNWState:
    news_doc = state["news_doc"]
    relevance_results = process_news_stream(
        news_docs=[news_doc],
        top_k=20,
        min_score=RELEVANCE_THRESHOLD,
        client_segments=["hnw"],
    )
    state["relevance_results"] = relevance_results

    print(f"[HNW] Relevance results for {len(relevance_results)} news item(s)")
    return state

def filter_candidates(state: HNWState) -> HNWState:
    seen: set[str] = set()
    candidates: list[dict] = []
    for matched_clients in state["relevance_results"].values():
        for client in matched_clients:
            cid = client["client_id"]

            if cid not in seen and client["relevance_score"] >= RELEVANCE_THRESHOLD:
                seen.add(cid)
                candidates.append(client)
    state["candidate_clients"] = candidates

    print(f"[HNW] Candidates: {[c['client_id'] for c in candidates]}")
    return state

def create_insight_events(state: HNWState) -> HNWState:
    news_doc = state["news_doc"]
    events = []
    for client in state["candidate_clients"]:
        cid = client["client_id"]
        events.append({
            "client_id": cid,
            "client_name": client.get("client_name"),
            "news_doc_id": news_doc["id"],
            "partition_key": news_doc["id"],
            "news_title": news_doc.get("title"),
            "news_document": news_doc,
            "client_portfolio_document": client.get("client_portfolio_document", {}),
            "relevance_score": client["relevance_score"],
            "matched_isins": client.get("matched_isins", []),
            "matched_tags": client.get("matched_tags", []),
            "priority": "realtime",
            "source": "mas.hnw_workflow",
        })
    state["generate_insight_events"] = events

    print(f"[HNW] Created {len(events)} insight events")

    if events:
        _record_news_stage(
            news_doc,
            stage="mas_hnw",
            status="completed",
            details={"candidate_count": len(state["candidate_clients"])},
        )
        with EventExecutor() as executor:
            executor.publish_insight_events(events)
        _record_news_stage(
            news_doc,
            stage="generate_insight_queue",
            status="queued",
            details={"queued_events": len(events)},
        )
    else:
        _record_news_stage(
            news_doc,
            stage="mas_hnw",
            status="completed",
            details={"candidate_count": 0},
        )

    return state

def has_news_doc(state: HNWState) -> str:
    print(state.get("news_doc"))
    return "score" if state.get("news_doc") else END

def build_hnw_graph() -> StateGraph:
    g = StateGraph(HNWState)

    g.add_node("activate", hnw_agent_activation)
    g.add_node("fetch_news", fetch_news_document)
    g.add_node("score", score_relevance)
    g.add_node("filter", filter_candidates)
    g.add_node("create_events", create_insight_events)

    g.set_entry_point("activate")

    g.add_edge("activate", "fetch_news")

    g.add_conditional_edges(
        "fetch_news",
        has_news_doc,
        {"score": "score", END: END}
    )

    g.add_edge("score", "filter")
    g.add_edge("filter", "create_events")
    g.add_edge("create_events", END)

    return g.compile()

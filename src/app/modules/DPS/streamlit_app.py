import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
from azure.cosmos import CosmosClient

# Allow local `streamlit run src/app/modules/DPS/streamlit_app.py`
# to resolve imports from the `src` package root without requiring PYTHONPATH.
SRC_ROOT = Path(__file__).resolve().parents[3]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from app.modules.DPS.config.settings import settings


NEWS_STAGE_LABELS = {
    "dps_news_processor": "DPS processed",
    "change_feed_to_mas": "Queued to MAS",
    "mas_hnw": "MAS relevance",
    "generate_insight_queue": "Queued to IG",
    "generate_insight": "Insight generation",
}


st.set_page_config(page_title="SMIF News Operations", layout="wide")
st.title("SMIF News Operations Dashboard")
st.caption("Admin view of news documents moving from DPS into MAS and insight generation.")


@st.cache_resource
def get_cosmos_containers():
    client = CosmosClient(
        settings.COSMOS_URL,
        credential=settings.COSMOS_KEY,
        connection_verify=False,
        enable_endpoint_discovery=False,
        connection_timeout=5,
    )
    database = client.get_database_client(settings.COSMOS_DB)
    return (
        database.get_container_client(settings.NEWS_CONTAINER),
        database.get_container_client(settings.INSIGHTS_CONTAINER),
    )


@st.cache_data(ttl=5)
def load_news_rows(limit: int) -> list[dict]:
    news_container, _ = get_cosmos_containers()
    query = """
    SELECT TOP @limit
        c.id,
        c.title,
        c.source,
        c.symbols,
        c.published_at,
        c._ts,
        c.monitoring
    FROM c
    ORDER BY c._ts DESC
    """
    params = [{"name": "@limit", "value": limit}]
    return list(
        news_container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True,
        )
    )


@st.cache_data(ttl=5)
def count_news_documents() -> int:
    news_container, _ = get_cosmos_containers()
    return next(
        iter(
            news_container.query_items(
                query="SELECT VALUE COUNT(1) FROM c",
                enable_cross_partition_query=True,
            )
        ),
        0,
    )


@st.cache_data(ttl=5)
def count_news_by_stage(stage: str) -> int:
    news_container, _ = get_cosmos_containers()
    return next(
        iter(
            news_container.query_items(
                query=(
                    "SELECT VALUE COUNT(1) FROM c "
                    "WHERE IS_DEFINED(c.monitoring.current_stage) "
                    "AND c.monitoring.current_stage = @stage"
                ),
                parameters=[{"name": "@stage", "value": stage}],
                enable_cross_partition_query=True,
            )
        ),
        0,
    )


@st.cache_data(ttl=5)
def count_failed_news_documents() -> int:
    news_container, _ = get_cosmos_containers()
    return next(
        iter(
            news_container.query_items(
                query=(
                    "SELECT VALUE COUNT(1) FROM c "
                    "WHERE IS_DEFINED(c.monitoring.current_status) "
                    "AND c.monitoring.current_status = 'failed'"
                ),
                enable_cross_partition_query=True,
            )
        ),
        0,
    )


@st.cache_data(ttl=5)
def load_recent_insights(limit: int) -> list[dict]:
    _, insights_container = get_cosmos_containers()
    query = """
    SELECT TOP @limit
        c.client_id,
        c.news_doc_id,
        c.news_title,
        c.status,
        c.verification_score,
        c.timestamp
    FROM c
    ORDER BY c._ts DESC
    """
    params = [{"name": "@limit", "value": limit}]
    return list(
        insights_container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True,
        )
    )


@st.cache_data(ttl=5)
def count_insights() -> int:
    _, insights_container = get_cosmos_containers()
    return next(
        iter(
            insights_container.query_items(
                query="SELECT VALUE COUNT(1) FROM c",
                enable_cross_partition_query=True,
            )
        ),
        0,
    )


def format_stage(stage: str | None) -> str:
    if not stage:
        return "Untracked"
    return NEWS_STAGE_LABELS.get(stage, stage.replace("_", " ").title())


def format_timestamp(value: str | None, fallback_ts: int | None = None) -> str:
    if value:
        return value
    if fallback_ts:
        return datetime.fromtimestamp(fallback_ts, tz=timezone.utc).isoformat()
    return "-"


def build_news_table(rows: list[dict]) -> pd.DataFrame:
    table_rows = []
    for row in rows:
        monitoring = row.get("monitoring") or {}
        symbols = row.get("symbols") or []
        table_rows.append(
            {
                "news_id": row.get("id"),
                "title": row.get("title") or "Untitled",
                "source": row.get("source") or "-",
                "symbols": ", ".join(symbols[:5]) if symbols else "-",
                "stage": format_stage(monitoring.get("current_stage")),
                "status": monitoring.get("current_status", "unknown"),
                "updated_at": format_timestamp(monitoring.get("updated_at"), row.get("_ts")),
                "published_at": format_timestamp(row.get("published_at")),
            }
        )
    return pd.DataFrame(table_rows)


def build_timeline_table(row: dict) -> pd.DataFrame:
    monitoring = row.get("monitoring") or {}
    timeline = monitoring.get("timeline") or []
    events = []
    for item in reversed(timeline):
        details = item.get("details") or {}
        events.append(
            {
                "timestamp": item.get("timestamp"),
                "stage": format_stage(item.get("stage")),
                "status": item.get("status"),
                "details": json.dumps(details, ensure_ascii=True) if details else "-",
            }
        )
    return pd.DataFrame(events)


def render_dashboard(limit: int, insight_limit: int) -> None:
    total_news = count_news_documents()
    queued_to_mas = count_news_by_stage("change_feed_to_mas")
    active_generation = count_news_by_stage("generate_insight")
    total_insights = count_insights()
    failed_news = count_failed_news_documents()

    metric_cols = st.columns(5)
    metric_cols[0].metric("News Docs", total_news)
    metric_cols[1].metric("Queued To MAS", queued_to_mas)
    metric_cols[2].metric("In Insight Gen", active_generation)
    metric_cols[3].metric("Insights Saved", total_insights)
    metric_cols[4].metric("Failed", failed_news)

    news_rows = load_news_rows(limit)
    news_df = build_news_table(news_rows)

    left, right = st.columns([2.3, 1.2])
    with left:
        st.subheader("Live News Lifecycle")
        if news_df.empty:
            st.info("No news documents found in Cosmos.")
        else:
            st.dataframe(news_df, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Recent Insight Outputs")
        recent_insights = load_recent_insights(insight_limit)
        if recent_insights:
            st.dataframe(pd.DataFrame(recent_insights), use_container_width=True, hide_index=True)
        else:
            st.info("No insights generated yet.")

    if news_rows:
        st.subheader("Selected News Timeline")
        selection_options = {
            f"{row.get('id')} | {row.get('title') or 'Untitled'}": row
            for row in news_rows
        }
        selected_label = st.selectbox("Inspect document", list(selection_options.keys()))
        selected_row = selection_options[selected_label]
        selected_monitoring = selected_row.get("monitoring") or {}

        summary_cols = st.columns(4)
        summary_cols[0].caption(f"Current stage: {format_stage(selected_monitoring.get('current_stage'))}")
        summary_cols[1].caption(f"Current status: {selected_monitoring.get('current_status', 'unknown')}")
        summary_cols[2].caption(f"Published at: {format_timestamp(selected_row.get('published_at'))}")
        summary_cols[3].caption(f"Last update: {format_timestamp(selected_monitoring.get('updated_at'), selected_row.get('_ts'))}")

        timeline_df = build_timeline_table(selected_row)
        if timeline_df.empty:
            st.info("This document does not have lifecycle events yet.")
        else:
            st.dataframe(timeline_df, use_container_width=True, hide_index=True)


def load_json_files(files):
    docs = []
    for uploaded_file in files:
        data = json.load(uploaded_file)
        if isinstance(data, list):
            docs.extend(data)
        else:
            docs.append(data)
    return docs


def load_json_from_folder(folder_path):
    docs = []
    path = Path(folder_path)
    for file in path.glob("*.json"):
        with open(file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            docs.extend(data)
        else:
            docs.append(data)
    return docs


with st.sidebar:
    refresh_seconds = st.slider("Refresh every (seconds)", min_value=5, max_value=60, value=10, step=5)
    news_limit = st.slider("News rows", min_value=10, max_value=200, value=50, step=10)
    insight_limit = st.slider("Insight rows", min_value=5, max_value=50, value=10, step=5)
    if st.button("Refresh now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


if hasattr(st, "fragment"):
    @st.fragment(run_every=f"{refresh_seconds}s")
    def render_live_dashboard() -> None:
        render_dashboard(news_limit, insight_limit)

    render_live_dashboard()
else:
    render_dashboard(news_limit, insight_limit)


with st.expander("Manual DPS Ingestion", expanded=False):
    st.write("Upload JSON files or run the local sample set through the DPS pipeline.")
    input_mode = st.radio("Choose Input Source", ["Upload JSON Files", "Run Sample Files"], horizontal=True)

    if input_mode == "Upload JSON Files":
        uploaded_files = st.file_uploader(
            "Upload JSON Files",
            type=["json"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)} files uploaded")
            if st.button("Start Data Pipeline"):
                from app.modules.DPS.pipeline import run_pipeline

                with st.spinner("Processing files through pipeline..."):
                    docs = load_json_files(uploaded_files)
                    st.write(f"Total documents detected: {len(docs)}")
                    try:
                        pipeline_result = asyncio.run(run_pipeline(docs))
                        st.success("Pipeline completed successfully")
                        st.json(
                            {
                                "documents_processed": len(docs),
                                "pipeline_status": pipeline_result,
                            }
                        )
                        st.cache_data.clear()
                    except Exception as exc:
                        st.error("Pipeline execution failed")
                        st.exception(exc)

    if input_mode == "Run Sample Files":
        sample_folder = Path(__file__).resolve().parent / "news_raw"
        if st.button("Run Sample Pipeline"):
            from app.modules.DPS.pipeline import run_pipeline

            with st.spinner("Processing sample files..."):
                docs = load_json_from_folder(sample_folder)
                st.write(f"Sample documents detected: {len(docs)}")
                try:
                    pipeline_result = asyncio.run(run_pipeline(docs))
                    st.success("Pipeline completed successfully")
                    st.json(
                        {
                            "documents_processed": len(docs),
                            "pipeline_status": pipeline_result,
                        }
                    )
                    st.cache_data.clear()
                except Exception as exc:
                    st.error("Pipeline execution failed")
                    st.exception(exc)

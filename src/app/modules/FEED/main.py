import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from azure.cosmos import CosmosClient


SRC_ROOT = Path(__file__).resolve().parents[3]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from app.modules.FEED.settings import settings


st.set_page_config(page_title="SMIF Clients", layout="wide")
st.title("SMIF Clients")


@st.cache_resource
def get_cosmos_client() -> CosmosClient:
    return CosmosClient(
        url=settings.COSMOS_URL,
        credential=settings.COSMOS_KEY,
        connection_verify=False,
        enable_endpoint_discovery=False,
        connection_timeout=5,
    )


def get_container(container_name: str):
    client = get_cosmos_client()
    return (
        client.get_database_client(settings.COSMOS_DB)
        .get_container_client(container_name)
    )


@st.cache_data(ttl=30)
def load_clients() -> list[dict]:
    container = get_container(settings.CLIENT_PORTFOLIO_CONTAINER)
    query = """
    SELECT c.client_id, c.client_name
    FROM c
    ORDER BY c.client_name
    """
    items = list(
        container.query_items(
            query=query,
            enable_cross_partition_query=True,
        )
    )
    deduped = {}
    for item in items:
        client_id = item.get("client_id")
        if client_id:
            deduped[client_id] = {
                "client_id": client_id,
                "client_name": item.get("client_name", client_id),
            }
    return list(deduped.values())


@st.cache_data(ttl=30)
def load_insights(client_id: str) -> list[dict]:
    container = get_container(settings.INSIGHTS_CONTAINER)
    query = """
    SELECT c.id, c.client_id, c.insight, c.verification_score,
           c.news_title, c.tickers, c.status, c.timestamp
    FROM c
    WHERE c.client_id = @client_id
    ORDER BY c.timestamp DESC
    """
    return list(
        container.query_items(
            query=query,
            parameters=[{"name": "@client_id", "value": client_id}],
            partition_key=client_id,
        )
    )


@st.cache_data(ttl=30)
def load_client_portfolio(client_id: str) -> dict | None:
    container = get_container(settings.CLIENT_PORTFOLIO_CONTAINER)
    query = """
    SELECT TOP 1 *
    FROM c
    WHERE c.client_id = @client_id
    """
    items = list(
        container.query_items(
            query=query,
            parameters=[{"name": "@client_id", "value": client_id}],
            partition_key=client_id,
        )
    )
    return items[0] if items else None


def render_insight_card(insight: dict) -> None:
    title = insight.get("news_title") or "Untitled Insight"
    score = insight.get("verification_score")
    status = insight.get("status", "unknown")
    timestamp = insight.get("timestamp", "unknown")
    tickers = insight.get("tickers") or []

    with st.container(border=True):
        st.subheader(title)
        cols = st.columns(3)
        cols[0].caption(f"Status: {status}")
        cols[1].caption(f"Verification Score: {score}")
        cols[2].caption(f"Timestamp: {timestamp}")

        if tickers:
            st.caption("Tickers: " + ", ".join(tickers))

        st.write(insight.get("insight", "No insight text available."))


def _format_currency_amount(value: float | int | None) -> str:
    if value is None:
        return "-"
    numeric_value = float(value)
    if numeric_value >= 1_000_000:
        return f"AED {numeric_value / 1_000_000:,.2f}M"
    if numeric_value >= 1_000:
        return f"AED {numeric_value / 1_000:,.0f}K"
    return f"AED {numeric_value:,.0f}"


def _weights_frame(weights: dict | None, label: str) -> pd.DataFrame:
    entries = []
    for key, value in (weights or {}).items():
        entries.append({label: key, "Weight %": round(float(value) * 100, 2)})
    frame = pd.DataFrame(entries)
    if frame.empty:
        return frame
    return frame.sort_values("Weight %", ascending=False, ignore_index=True)


def render_portfolio_card(portfolio: dict | None) -> None:
    st.subheader("Client Portfolio")
    if not portfolio:
        st.info("No portfolio document found for this client.")
        return

    metric_cols = st.columns(4)
    metric_cols[0].metric("Client Type", portfolio.get("client_type", "-"))
    metric_cols[1].metric("Mandate", portfolio.get("mandate", "-"))
    metric_cols[2].metric("AUM", _format_currency_amount(portfolio.get("total_aum_aed")))
    metric_cols[3].metric("Tickers", len(portfolio.get("ticker_symbols") or []))

    summary_cols = st.columns(2)
    with summary_cols[0]:
        st.caption("Ticker Symbols")
        tickers = portfolio.get("ticker_symbols") or []
        st.write(", ".join(tickers) if tickers else "No ticker symbols available.")

        st.caption("Currencies")
        currencies = portfolio.get("currencies") or []
        st.write(", ".join(currencies) if currencies else "No currencies available.")

        st.caption("Tags Of Interest")
        tags = portfolio.get("tags_of_interest") or []
        st.write(", ".join(tags[:15]) if tags else "No derived tags available.")

    with summary_cols[1]:
        st.caption("Portfolio Summary")
        st.write(portfolio.get("query", "No portfolio summary available."))

    weight_cols = st.columns(2)
    with weight_cols[0]:
        st.caption("Asset Class Weights")
        classification_df = _weights_frame(
            portfolio.get("classification_weights"),
            "Asset Class",
        )
        if classification_df.empty:
            st.write("No asset class weights available.")
        else:
            st.dataframe(classification_df, use_container_width=True, hide_index=True)

    with weight_cols[1]:
        st.caption("Asset Type Weights")
        asset_type_df = _weights_frame(
            portfolio.get("asset_type_weights"),
            "Asset Type",
        )
        if asset_type_df.empty:
            st.write("No asset type weights available.")
        else:
            st.dataframe(asset_type_df, use_container_width=True, hide_index=True)

    holdings_cols = st.columns(2)
    with holdings_cols[0]:
        st.caption("Top Asset Descriptions")
        asset_descriptions = portfolio.get("asset_descriptions") or []
        if asset_descriptions:
            st.dataframe(
                pd.DataFrame({"Asset Description": asset_descriptions[:20]}),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("No asset descriptions available.")

    with holdings_cols[1]:
        st.caption("Identifiers")
        identifiers = pd.DataFrame(
            {
                "ISIN": portfolio.get("isins") or [],
            }
        )
        if identifiers.empty:
            st.write("No ISINs available.")
        else:
            st.dataframe(
                identifiers.head(20),
                use_container_width=True,
                hide_index=True,
            )


try:
    clients = load_clients()
except Exception as exc:
    st.error(f"Failed to load clients from Cosmos DB: {exc}")
    st.stop()

if not clients:
    st.info("No client profiles are available yet.")
    st.stop()


client_options = {
    f"{client['client_name']} ({client['client_id']})": client["client_id"]
    for client in clients
}

selected_label = st.selectbox("Select Client", list(client_options.keys()))
selected_client_id = client_options[selected_label]


try:
    portfolio = load_client_portfolio(selected_client_id)
    insights = load_insights(selected_client_id)
except Exception as exc:
    st.error(f"Failed to load portfolio or insights for client {selected_client_id}: {exc}")
    st.stop()

render_portfolio_card(portfolio)

st.subheader("Client Insights")
if not insights:
    st.info(f"No insights found for client {selected_client_id}.")
else:
    st.write(f"Showing {len(insights)} insight(s) for client `{selected_client_id}`.")
    for insight in insights:
        render_insight_card(insight)

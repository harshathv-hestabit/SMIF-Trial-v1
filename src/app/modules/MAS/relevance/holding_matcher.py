from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

from app.common.azure_services.cosmos import (
    build_sync_cosmos_client,
    get_container_client,
    get_database_client,
)
from app.common.portfolio_schema import (
    build_holdings_container_name,
    build_holdings_snapshot_document_id,
)

from ..config.search import _extract_news_features, _normalize_keyword, _normalize_ticker
from ..config.settings import settings


MATCH_BASE_SCORES = {
    "direct_isin": 1.00,
    "direct_ticker": 0.95,
    "direct_underlying": 0.90,
    "direct_issuer": 0.85,
    "indirect_currency": 0.45,
    "indirect_macro_allocation": 0.40,
}
MAX_INCLUDED_HOLDINGS = 10

_cosmos_client = build_sync_cosmos_client(settings.COSMOS_URL, settings.COSMOS_KEY)


def ground_candidate_against_holdings(
    *,
    news_doc: dict,
    candidate: dict,
    max_matched_holdings: int = MAX_INCLUDED_HOLDINGS,
) -> dict[str, Any]:
    client_id = str(candidate.get("client_id", "")).strip()
    profile = candidate.get("search_relevance_profile", {}) or {}
    snapshot_id = str(
        candidate.get("profile_snapshot_id")
        or profile.get("snapshot_id")
        or ""
    ).strip()
    snapshot = _load_holdings_snapshot(client_id=client_id, snapshot_id=snapshot_id)
    holdings = snapshot.get("holdings", []) if isinstance(snapshot, dict) else []
    news_features = _extract_news_features(news_doc)
    supported_currencies = _collect_supported_currencies(
        profile=profile,
        holdings=holdings if isinstance(holdings, list) else [],
    )
    matches = _match_holdings(
        holdings=holdings if isinstance(holdings, list) else [],
        news_doc=news_doc,
        news_features=news_features,
        candidate=candidate,
        supported_currencies=supported_currencies,
    )

    direct_count = sum(1 for item in matches if item["directness"] == "direct")
    indirect_count = sum(1 for item in matches if item["directness"] == "indirect")
    included = matches[:max(max_matched_holdings, 1)]
    grounded_relevance = "none"
    if direct_count:
        grounded_relevance = "direct"
    elif indirect_count:
        grounded_relevance = "indirect"
    snapshot_as_of = profile.get("as_of")
    if not snapshot_as_of and isinstance(snapshot, dict):
        snapshot_as_of = snapshot.get("as_of")
    representation_version = profile.get("representation_version")
    if not representation_version and isinstance(snapshot, dict):
        representation_version = snapshot.get("representation_version")

    return {
        "client_id": client_id,
        "snapshot_id": snapshot_id,
        "portfolio_snapshot": {
            "snapshot_id": snapshot_id,
            "as_of": snapshot_as_of,
            "representation_version": representation_version,
        },
        "holding_match_summary": {
            "direct_match_count": direct_count,
            "indirect_match_count": indirect_count,
            "top_match_score": included[0]["match_score"] if included else 0.0,
            "client_grounded_relevance": grounded_relevance,
        },
        "matched_holdings": included,
        "overflow": {
            "matched_holding_count_total": len(matches),
            "matched_holding_count_included": len(included),
        },
    }


def build_client_profile_summary(profile: dict[str, Any]) -> dict[str, Any]:
    asset_class_weights = profile.get("asset_class_weights") or profile.get("classification_weights") or {}
    return {
        "client_type": profile.get("client_type"),
        "client_segment": profile.get("client_segment"),
        "mandate": profile.get("mandate"),
        "total_aum_aed": profile.get("total_aum_aed"),
        "asset_class_weights": asset_class_weights,
        "asset_type_weights": profile.get("asset_type_weights") or {},
        "currencies": profile.get("currencies") or [],
    }


def build_relevance_payload(candidate: dict[str, Any], grounding: dict[str, Any]) -> dict[str, Any]:
    holding_summary = grounding.get("holding_match_summary", {}) if isinstance(grounding, dict) else {}
    overflow = grounding.get("overflow", {}) if isinstance(grounding, dict) else {}
    return {
        "candidate_score": float(candidate.get("candidate_score", candidate.get("relevance_score", 0.0)) or 0.0),
        "grounded_relevance": holding_summary.get("client_grounded_relevance", "none"),
        "candidate_reasons": candidate.get("candidate_reasons", []),
        "matched_holding_count_total": overflow.get("matched_holding_count_total", 0),
        "matched_holding_count_included": overflow.get("matched_holding_count_included", 0),
    }


def build_compact_portfolio_context_from_grounding(
    *,
    news_doc: dict[str, Any],
    profile: dict[str, Any],
    grounding: dict[str, Any],
) -> dict[str, Any]:
    news_symbols = {
        _normalize_ticker(symbol)
        for symbol in (news_doc.get("symbols") or [])
        if _normalize_ticker(symbol)
    }
    relevant_holdings = []
    overlap: set[str] = set()
    for holding in grounding.get("matched_holdings", []) if isinstance(grounding, dict) else []:
        ticker = _normalize_ticker(
            holding.get("ticker") or holding.get("underlying_ticker") or ""
        )
        if ticker and ticker in news_symbols:
            overlap.add(ticker)
        display_ticker = (
            holding.get("ticker")
            or holding.get("underlying_ticker")
            or holding.get("currency")
            or holding.get("asset_id")
            or "-"
        )
        relevant_holdings.append(
            {
                "ticker": display_ticker,
                "description": holding.get("description", ""),
                "match_type": holding.get("match_type", ""),
                "match_score": holding.get("match_score"),
            }
        )

    summary = build_client_profile_summary(profile)
    return {
        "client_type": summary.get("client_type", ""),
        "mandate": summary.get("mandate", ""),
        "total_aum_aed": summary.get("total_aum_aed"),
        "asset_type_weights": summary.get("asset_type_weights", {}),
        "classification_weights": summary.get("asset_class_weights", {}),
        "currencies": (summary.get("currencies") or [])[:5],
        "relevant_holdings": relevant_holdings,
        "news_symbol_overlap": sorted(overlap),
        "grounded_relevance": grounding.get("holding_match_summary", {}).get("client_grounded_relevance", "none")
        if isinstance(grounding, dict)
        else "none",
    }


def _holdings_container():
    database = get_database_client(_cosmos_client, settings.COSMOS_DB)
    return get_container_client(
        database,
        build_holdings_container_name(settings.CLIENT_PORTFOLIO_CONTAINER),
    )


def _load_holdings_snapshot(*, client_id: str, snapshot_id: str) -> dict[str, Any]:
    if not client_id:
        return {}
    container = _holdings_container()
    if snapshot_id:
        try:
            return container.read_item(
                item=build_holdings_snapshot_document_id(snapshot_id),
                partition_key=client_id,
            )
        except CosmosResourceNotFoundError:
            return {}
        except CosmosHttpResponseError:
            return {}

    try:
        items = list(
            container.query_items(
                query="""
                SELECT TOP 1 * FROM c
                WHERE c.client_id = @client_id
                ORDER BY c.as_of DESC
                """,
                parameters=[{"name": "@client_id", "value": client_id}],
                partition_key=client_id,
            )
        )
    except CosmosHttpResponseError:
        return {}
    return items[0] if items else {}


def _match_holdings(
    *,
    holdings: list[dict[str, Any]],
    news_doc: dict[str, Any],
    news_features: dict[str, Any],
    candidate: dict[str, Any],
    supported_currencies: set[str],
) -> list[dict[str, Any]]:
    news_text = " ".join(
        [
            str(news_doc.get("title") or ""),
            str(news_doc.get("teaser") or ""),
            str(news_doc.get("content") or ""),
            " ".join(str(tag) for tag in (news_doc.get("tags") or [])),
            " ".join(str(symbol) for symbol in (news_doc.get("symbols") or [])),
        ]
    ).upper()
    news_tickers = set(news_features.get("news_tickers", []))
    matched_classifications = {
        _normalize_keyword(value)
        for value in candidate.get("matched_classifications", [])
        if _normalize_keyword(value)
    }
    mentioned_currencies = _extract_currencies(news_text, supported_currencies)

    matches: list[dict[str, Any]] = []
    for holding in holdings:
        match = _match_single_holding(
            holding=holding,
            news_text=news_text,
            news_tickers=news_tickers,
            matched_classifications=matched_classifications,
            mentioned_currencies=mentioned_currencies,
        )
        if match is not None:
            matches.append(match)

    matches.sort(
        key=lambda item: (
            item["directness"] != "direct",
            -float(item["match_score"]),
            -float(item.get("portfolio_weight") or 0.0),
            -float(item.get("market_value_aed") or 0.0),
            str(item.get("holding_id") or ""),
        )
    )
    return matches


def _match_single_holding(
    *,
    holding: dict[str, Any],
    news_text: str,
    news_tickers: set[str],
    matched_classifications: set[str],
    mentioned_currencies: set[str],
) -> dict[str, Any] | None:
    isin = _normalize_keyword(holding.get("isin"))
    ticker = _normalize_ticker(holding.get("ticker"))
    underlying_ticker = _normalize_ticker(holding.get("underlying_ticker"))
    issuer = _normalize_keyword(holding.get("issuer_normalized") or holding.get("issuer_name"))
    description = _normalize_keyword(holding.get("description"))
    classification = _normalize_keyword(holding.get("classification"))
    holding_currencies = _holding_currency_values(holding)

    match_type = ""
    reasons: list[str] = []
    directness = "indirect"

    if isin and isin in news_text:
        match_type = "direct_isin"
        directness = "direct"
        reasons.extend([f"news_isin={isin}", f"holding_isin={isin}"])
    elif ticker and ticker in news_tickers:
        match_type = "direct_ticker"
        directness = "direct"
        reasons.extend([f"news_ticker={ticker}", f"holding_ticker={ticker}"])
        if ticker and ticker in description:
            reasons.append(f"description_contains_{ticker.lower()}")
    elif underlying_ticker and underlying_ticker in news_tickers:
        match_type = "direct_underlying"
        directness = "direct"
        reasons.extend(
            [
                f"news_ticker={underlying_ticker}",
                f"holding_underlying_ticker={underlying_ticker}",
            ]
        )
        if underlying_ticker and underlying_ticker in description:
            reasons.append(f"description_contains_{underlying_ticker.lower()}")
    elif issuer and _issuer_matches(issuer, news_text):
        match_type = "direct_issuer"
        directness = "direct"
        reasons.extend([f"news_issuer={issuer}", f"holding_issuer={issuer}"])
    elif holding_currencies and mentioned_currencies and holding_currencies & mentioned_currencies:
        matched_currency = sorted(holding_currencies & mentioned_currencies)[0]
        match_type = "indirect_currency"
        reasons.extend(
            [
                f"news_currency={matched_currency}",
                f"holding_currency={matched_currency}",
            ]
        )
    elif classification and classification in matched_classifications:
        match_type = "indirect_macro_allocation"
        reasons.extend(
            [
                f"news_classification={classification}",
                f"holding_classification={classification}",
            ]
        )
    else:
        return None

    base_score = MATCH_BASE_SCORES[match_type]
    materiality_modifier = min(float(holding.get("portfolio_weight") or 0.0) * 0.5, 0.05)
    reason_bonus = min(max(len(reasons) - 1, 0) * 0.02, 0.04)
    final_score = round(min(base_score + materiality_modifier + reason_bonus, 0.99), 4)

    return {
        "holding_id": holding.get("holding_id"),
        "asset_id": holding.get("asset_id"),
        "isin": holding.get("isin"),
        "ticker": holding.get("ticker"),
        "description": holding.get("description"),
        "asset_type": holding.get("asset_type"),
        "asset_subtype": holding.get("asset_subtype"),
        "classification": holding.get("classification"),
        "currency": holding.get("currency"),
        "market_value_aed": holding.get("market_value_aed"),
        "portfolio_weight": holding.get("portfolio_weight"),
        "underlying_ticker": holding.get("underlying_ticker"),
        "match_type": match_type,
        "directness": directness,
        "match_score": final_score,
        "match_reasons": reasons,
    }


def _issuer_matches(issuer: str, news_text: str) -> bool:
    if not issuer:
        return False
    if issuer in news_text:
        return True
    tokens = [token for token in issuer.split() if len(token) > 2]
    if len(tokens) >= 2:
        return all(token in news_text for token in tokens[:2])
    return bool(tokens and tokens[0] in news_text)


def _extract_currencies(news_text: str, supported_currencies: set[str]) -> set[str]:
    if not supported_currencies:
        return set()
    return {currency for currency in supported_currencies if currency in news_text}


def _collect_supported_currencies(
    *,
    profile: dict[str, Any],
    holdings: list[dict[str, Any]],
) -> set[str]:
    currencies = {
        _normalize_keyword(currency)
        for currency in (profile.get("currencies") or [])
        if _normalize_keyword(currency)
    }
    for holding in holdings:
        if not isinstance(holding, dict):
            continue
        currencies.update(_holding_currency_values(holding))
    return currencies


def _holding_currency_values(holding: dict[str, Any]) -> set[str]:
    values = holding.get("currency_values")
    if isinstance(values, list):
        return {
            _normalize_keyword(value)
            for value in values
            if _normalize_keyword(value)
        }
    raw_currency = _normalize_keyword(holding.get("currency"))
    if not raw_currency:
        return set()
    if "," not in raw_currency:
        return {raw_currency}
    return {
        _normalize_keyword(part)
        for part in raw_currency.split(",")
        if _normalize_keyword(part)
    }

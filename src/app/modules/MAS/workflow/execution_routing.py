from __future__ import annotations

from typing import Any, Literal

from ..config.search import _normalize_keyword, _normalize_ticker
from ..config.settings import settings


ExecutionRoute = Literal["full_loop", "single_pass_indirect", "skip"]


def assign_execution_route(
    *,
    news_doc: dict[str, Any],
    candidate: dict[str, Any],
    grounding: dict[str, Any],
    compact_context: dict[str, Any] | None = None,
) -> dict[str, Any]:

    summary = grounding.get("holding_match_summary", {}) if isinstance(grounding, dict) else {}
    overflow = grounding.get("overflow", {}) if isinstance(grounding, dict) else {}

    grounded_relevance = str(summary.get("client_grounded_relevance") or "none")
    direct_match_count = int(summary.get("direct_match_count", 0) or 0)
    indirect_match_count = int(summary.get("indirect_match_count", 0) or 0)
    top_match_score = float(summary.get("top_match_score", 0.0) or 0.0)
    matched_holdings_count = int(
        overflow.get(
            "matched_holding_count_total",
            len(grounding.get("matched_holdings", []) if isinstance(grounding, dict) else []),
        )
        or 0
    )
    matched_symbols = _derive_matched_symbols(
        news_doc=news_doc,
        grounding=grounding,
        compact_context=compact_context or {},
    )
    security_type_alignment = _derive_security_type_alignment(
        candidate=candidate,
        grounding=grounding,
    )

    indirect_min_score = float(settings.EXECUTION_ROUTE_INDIRECT_MIN_TOP_MATCH_SCORE)
    indirect_min_holdings = max(int(settings.EXECUTION_ROUTE_INDIRECT_MIN_MATCHED_HOLDINGS), 1)
    skip_on_mismatch = bool(settings.EXECUTION_ROUTE_SKIP_ON_SECURITY_TYPE_MISMATCH)

    route: ExecutionRoute
    reason: str

    if grounded_relevance == "direct" or direct_match_count > 0 or matched_symbols:
        route = "full_loop"
        reason = "Direct grounded exposure with matched holdings and security-level overlap."
    elif grounded_relevance != "indirect" or indirect_match_count <= 0:
        route = "skip"
        reason = "Grounded candidate did not retain actionable direct or indirect exposure."
    elif matched_holdings_count < indirect_min_holdings:
        route = "skip"
        reason = (
            "Indirect grounding below matched-holdings threshold "
            f"({matched_holdings_count} < {indirect_min_holdings})."
        )
    elif security_type_alignment is False and skip_on_mismatch:
        route = "skip"
        reason = "Indirect grounding present but matched holdings are not aligned with the inferred security type."
    elif top_match_score < indirect_min_score:
        route = "skip"
        reason = (
            "Indirect grounding below generation threshold "
            f"({top_match_score:.2f} < {indirect_min_score:.2f})."
        )
    else:
        route = "single_pass_indirect"
        reason = "Indirect allocation-level relevance only; no direct matched holding."

    return {
        "execution_route": route,
        "route_reason": reason,
        "grounded_relevance": grounded_relevance,
        "matched_holdings_count": matched_holdings_count,
        "matched_symbols": matched_symbols,
        "security_type_alignment": security_type_alignment,
        "direct_matched_holdings_count": direct_match_count,
        "indirect_matched_holdings_count": indirect_match_count,
        "top_match_score": top_match_score,
        "verifier_enabled": route == "full_loop",
    }


def _derive_matched_symbols(
    *,
    news_doc: dict[str, Any],
    grounding: dict[str, Any],
    compact_context: dict[str, Any],
) -> list[str]:
    overlap = compact_context.get("news_symbol_overlap")
    if isinstance(overlap, list) and overlap:
        return sorted(
            {
                _normalize_ticker(symbol)
                for symbol in overlap
                if _normalize_ticker(symbol)
            }
        )

    news_symbols = {
        _normalize_ticker(symbol)
        for symbol in (news_doc.get("symbols") or [])
        if _normalize_ticker(symbol)
    }
    matched_symbols: set[str] = set()
    for holding in grounding.get("matched_holdings", []) if isinstance(grounding, dict) else []:
        ticker = _normalize_ticker(holding.get("ticker"))
        underlying_ticker = _normalize_ticker(holding.get("underlying_ticker"))
        if ticker and ticker in news_symbols:
            matched_symbols.add(ticker)
        if underlying_ticker and underlying_ticker in news_symbols:
            matched_symbols.add(underlying_ticker)
    return sorted(matched_symbols)


def _derive_security_type_alignment(
    *,
    candidate: dict[str, Any],
    grounding: dict[str, Any],
) -> bool | None:
    matched_holdings = grounding.get("matched_holdings", []) if isinstance(grounding, dict) else []
    if any(str(holding.get("directness") or "") == "direct" for holding in matched_holdings):
        return True

    matched_classifications = {
        _normalize_keyword(value)
        for value in candidate.get("matched_classifications", [])
        if _normalize_keyword(value)
    }
    holding_classifications = {
        _normalize_keyword(holding.get("classification"))
        for holding in matched_holdings
        if _normalize_keyword(holding.get("classification"))
    }

    if matched_classifications and holding_classifications:
        return bool(matched_classifications & holding_classifications)
    return None

from __future__ import annotations

import json
import re
from typing import Any


_SYMBOL_CLEAN_RE = re.compile(r"[^A-Z0-9]")


def _normalize_symbol(value: object | None) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return ""
    text = text.split(".")[0]
    text = text.split(" ")[0]
    return _SYMBOL_CLEAN_RE.sub("", text)


def _build_holdings(portfolio: dict[str, Any]) -> list[dict[str, str]]:
    matched_holdings = portfolio.get("matched_holdings") or portfolio.get("relevant_holdings") or []
    if isinstance(matched_holdings, list) and matched_holdings:
        holdings: list[dict[str, str]] = []
        for holding in matched_holdings:
            if not isinstance(holding, dict):
                continue
            ticker_value = (
                holding.get("ticker")
                or holding.get("underlying_ticker")
                or ""
            )
            ticker = str(ticker_value or "").strip()
            if not ticker:
                continue
            description = str(holding.get("description") or "").strip()
            holdings.append(
                {
                    "ticker": ticker,
                    "description": description,
                    "symbol": _normalize_symbol(ticker),
                }
            )
        if holdings:
            return holdings

    canonical_holdings = portfolio.get("holdings") or []
    if isinstance(canonical_holdings, list) and canonical_holdings:
        holdings: list[dict[str, str]] = []
        for holding in canonical_holdings:
            if not isinstance(holding, dict):
                continue
            ticker_value = holding.get("ticker") or holding.get("underlying_ticker") or ""
            ticker = str(ticker_value or "").strip()
            if not ticker:
                continue
            description = str(holding.get("description") or "").strip()
            holdings.append(
                {
                    "ticker": ticker,
                    "description": description,
                    "symbol": _normalize_symbol(ticker),
                }
            )
        if holdings:
            return holdings

    tickers = portfolio.get("ticker_symbols") or []
    descriptions = portfolio.get("asset_descriptions") or []

    if not isinstance(tickers, list):
        tickers = []
    if not isinstance(descriptions, list):
        descriptions = []

    holdings: list[dict[str, str]] = []
    for idx, ticker_value in enumerate(tickers):
        ticker = str(ticker_value or "").strip()
        if not ticker:
            continue
        description = ""
        if idx < len(descriptions):
            description = str(descriptions[idx] or "").strip()
        holdings.append(
            {
                "ticker": ticker,
                "description": description,
                "symbol": _normalize_symbol(ticker),
            }
        )
    return holdings


def _score_holding(
    holding: dict[str, str],
    *,
    news_symbols: set[str],
    matched_symbols: set[str],
    news_text: str,
) -> int:
    symbol = holding.get("symbol", "")
    if not symbol:
        return 0

    score = 0
    if symbol in matched_symbols:
        score += 100
    if symbol in news_symbols:
        score += 80
    if symbol and symbol in news_text:
        score += 25
    return score


def _safe_float(value: object | None) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _trim_list(values: object, limit: int) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(value).strip() for value in values if str(value).strip()][:limit]


def _raw_portfolio_char_estimate(portfolio: dict[str, Any]) -> int:
    fields = {
        "client_type": portfolio.get("client_type"),
        "mandate": portfolio.get("mandate"),
        "total_aum_aed": portfolio.get("total_aum_aed"),
        "asset_types": portfolio.get("asset_types"),
        "asset_subtypes": portfolio.get("asset_subtypes"),
        "asset_classifications": portfolio.get("asset_classifications"),
        "currencies": portfolio.get("currencies"),
        "isins": portfolio.get("isins"),
        "ticker_symbols": portfolio.get("ticker_symbols"),
        "major_tickers": portfolio.get("major_tickers"),
        "asset_descriptions": portfolio.get("asset_descriptions"),
        "classification_weights": portfolio.get("classification_weights") or portfolio.get("asset_class_weights"),
        "asset_type_weights": portfolio.get("asset_type_weights"),
        "matched_holdings": portfolio.get("matched_holdings"),
        "relevant_holdings": portfolio.get("relevant_holdings"),
    }
    return len(json.dumps(fields, ensure_ascii=False, separators=(",", ":")))


def build_compact_portfolio_context(
    *,
    news: dict[str, Any],
    portfolio: dict[str, Any],
    matched_symbols_from_event: list[str] | None = None,
    max_relevant_holdings: int = 10,
    fallback_holdings: int = 5,
    max_currencies: int = 5,
) -> tuple[dict[str, Any], dict[str, Any]]:
    news_symbols = {
        _normalize_symbol(symbol)
        for symbol in (news.get("symbols") or [])
        if _normalize_symbol(symbol)
    }
    matched_symbols = {
        _normalize_symbol(symbol)
        for symbol in (matched_symbols_from_event or [])
        if _normalize_symbol(symbol)
    }
    news_text = " ".join(
        [
            str(news.get("title") or ""),
            str(news.get("teaser") or ""),
            " ".join(str(tag) for tag in (news.get("tags") or [])),
        ]
    ).upper()

    holdings = _build_holdings(portfolio)
    scored: list[tuple[int, dict[str, str]]] = []
    for holding in holdings:
        score = _score_holding(
            holding,
            news_symbols=news_symbols,
            matched_symbols=matched_symbols,
            news_text=news_text,
        )
        if score > 0:
            scored.append((score, holding))

    scored.sort(key=lambda item: (-item[0], item[1]["ticker"]))
    selected = [item[1] for item in scored[:max_relevant_holdings]]

    if not selected:
        selected = holdings[:fallback_holdings]

    compact = {
        "client_type": str(portfolio.get("client_type") or ""),
        "mandate": str(portfolio.get("mandate") or ""),
        "total_aum_aed": _safe_float(portfolio.get("total_aum_aed")),
        "asset_type_weights": portfolio.get("asset_type_weights") or {},
        "classification_weights": portfolio.get("classification_weights")
        or portfolio.get("asset_class_weights")
        or {},
        "currencies": _trim_list(portfolio.get("currencies"), max_currencies),
        "relevant_holdings": [
            {
                "ticker": holding.get("ticker", ""),
                "description": holding.get("description", ""),
            }
            for holding in selected
        ],
        "news_symbol_overlap": sorted(news_symbols & matched_symbols),
        "grounded_relevance": str(portfolio.get("grounded_relevance") or ""),
    }

    compact_chars = len(json.dumps(compact, ensure_ascii=False, separators=(",", ":")))
    raw_chars = _raw_portfolio_char_estimate(portfolio)
    savings = max(raw_chars - compact_chars, 0)
    savings_pct = round((savings / raw_chars) * 100, 2) if raw_chars else 0.0

    profile = {
        "raw_portfolio_chars_estimate": raw_chars,
        "compact_portfolio_chars_estimate": compact_chars,
        "estimated_char_savings": savings,
        "estimated_char_savings_pct": savings_pct,
        "raw_counts": {
            "tickers": len(portfolio.get("ticker_symbols") or portfolio.get("major_tickers") or []),
            "isins": len(portfolio.get("isins") or []),
            "asset_descriptions": len(
                portfolio.get("asset_descriptions")
                or portfolio.get("major_asset_descriptions")
                or []
            ),
            "currencies": len(portfolio.get("currencies") or []),
        },
        "compact_counts": {
            "currencies": len(compact["currencies"]),
            "relevant_holdings": len(compact["relevant_holdings"]),
            "news_symbol_overlap": len(compact["news_symbol_overlap"]),
        },
    }
    return compact, profile


def format_holdings_for_prompt(holdings: list[dict[str, str]]) -> str:
    if not holdings:
        return "- No direct matched holdings identified."
    lines = []
    for idx, holding in enumerate(holdings, start=1):
        ticker = holding.get("ticker", "")
        description = holding.get("description", "")
        if description:
            lines.append(f"{idx}. {ticker} | {description}")
        else:
            lines.append(f"{idx}. {ticker}")
    return "\n".join(lines)

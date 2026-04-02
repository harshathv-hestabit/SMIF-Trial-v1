import json
import re
from langchain_core.messages import HumanMessage
from ..config import get_llm
from ..util.insight_logging import append_insight_log
from ..util.portfolio_compactor import (
    build_compact_portfolio_context,
    format_holdings_for_prompt,
)

llm = get_llm()
MAX_GUIDANCE_ITEMS = 3
MAX_GUIDANCE_WORDS = 18


def _needs_compaction(value: object) -> bool:
    if not isinstance(value, dict):
        return True
    required_keys = {
        "client_type",
        "mandate",
        "total_aum_aed",
        "asset_type_weights",
        "classification_weights",
        "currencies",
        "relevant_holdings",
    }
    return not required_keys.issubset(set(value.keys()))


def _record_token_usage(state: dict, *, agent: str, usage: dict) -> None:
    token_usage = state.setdefault(
        "token_usage",
        {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "calls": [],
        },
    )
    token_usage["prompt_tokens"] = int(token_usage.get("prompt_tokens", 0)) + int(
        usage.get("prompt_tokens", 0)
    )
    token_usage["completion_tokens"] = int(token_usage.get("completion_tokens", 0)) + int(
        usage.get("completion_tokens", 0)
    )
    token_usage["total_tokens"] = int(token_usage.get("total_tokens", 0)) + int(
        usage.get("total_tokens", 0)
    )
    token_usage.setdefault("calls", []).append(
        {
            "agent": agent,
            "iteration": state.get("iterations", 0),
            **usage,
        }
    )


def _extract_json_candidate(text: str) -> str:
    clean = text.strip()
    clean = clean.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    match = re.search(r"\{.*\}", clean, flags=re.DOTALL)
    if match:
        return match.group(0)
    return clean


def _coerce_score(value: object) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    return max(0.0, min(100.0, score))


def _derive_severity(score: float) -> str:
    if score >= 85:
        return "low"
    if score >= 70:
        return "medium"
    return "high"


def _normalize_short_item(value: object, *, max_words: int = MAX_GUIDANCE_WORDS) -> str:
    text = " ".join(str(value or "").strip().split())
    if not text:
        return ""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def _normalize_guidance_list(value: object) -> list[str]:
    if isinstance(value, list):
        raw_items = value
    elif value:
        raw_items = [value]
    else:
        raw_items = []

    normalized: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        cleaned = _normalize_short_item(item)
        lowered = cleaned.lower()
        if cleaned and lowered not in seen:
            normalized.append(cleaned)
            seen.add(lowered)
        if len(normalized) >= MAX_GUIDANCE_ITEMS:
            break
    return normalized


def _fallback_issue_from_feedback(feedback: str) -> str:
    compact = _normalize_short_item(feedback)
    return compact or "Insight quality issues detected."


def _parse_verifier_output(text: str) -> dict:
    candidate = _extract_json_candidate(text)
    try:
        parsed = json.loads(candidate)
    except Exception:
        fallback_full = str(text or "").strip() or "Verifier output parsing failed."
        return {
            "needs_revision": True,
            "score": 0.0,
            "severity": "high",
            "issues": ["Verifier output parsing failed."],
            "rewrite_guidance": ["Re-evaluate relevance, impact wording, and action cue."],
            "full_feedback": fallback_full,
        }

    score = _coerce_score(parsed.get("score", 0))
    severity_raw = str(parsed.get("severity", "")).strip().lower()
    severity = severity_raw if severity_raw in {"low", "medium", "high"} else _derive_severity(score)
    needs_revision_value = parsed.get("needs_revision", score < 75)
    if isinstance(needs_revision_value, bool):
        needs_revision = needs_revision_value
    elif isinstance(needs_revision_value, str):
        needs_revision = needs_revision_value.strip().lower() in {"true", "1", "yes"}
    else:
        needs_revision = bool(needs_revision_value)

    full_feedback = str(
        parsed.get("full_feedback")
        or parsed.get("feedback")
        or ""
    ).strip() or "No feedback provided."

    issues = _normalize_guidance_list(parsed.get("issues"))
    if not issues:
        issues = [_fallback_issue_from_feedback(full_feedback)]

    rewrite_guidance = _normalize_guidance_list(parsed.get("rewrite_guidance"))
    if not rewrite_guidance and needs_revision:
        rewrite_guidance = ["Address the issues above while preserving factual grounding."]

    return {
        "needs_revision": needs_revision,
        "score": score,
        "severity": severity,
        "issues": issues[:MAX_GUIDANCE_ITEMS],
        "rewrite_guidance": rewrite_guidance[:MAX_GUIDANCE_ITEMS],
        "full_feedback": full_feedback,
    }


async def verify_insight_agent(state: dict) -> dict:
    news = state["news_document"]
    portfolio = state["client_portfolio_document"]
    insight = state["insight_draft"]
    matched_symbols = state.get("matched_isins", [])

    compact_context = state.get("compact_portfolio_context")
    compact_profile = state.get("compact_portfolio_profile")
    if _needs_compaction(compact_context):
        compact_context, compact_profile = build_compact_portfolio_context(
            news=news,
            portfolio=portfolio,
            matched_symbols_from_event=matched_symbols if isinstance(matched_symbols, list) else [],
        )
        state["compact_portfolio_context"] = compact_context
        state["compact_portfolio_profile"] = compact_profile

    holdings_text = format_holdings_for_prompt(compact_context.get("relevant_holdings", []))

    prompt = f"""
You are a financial insight quality evaluator.

NEWS DOCUMENT
- Title: {news.get("title")}
- Teaser: {news.get("teaser")}
- Symbols: {news.get("symbols")}
- Tags: {news.get("tags")}

CLIENT PORTFOLIO SNAPSHOT
- Client Type: {compact_context.get("client_type")}
- Mandate: {compact_context.get("mandate")}
- Total AUM (aed): {compact_context.get("total_aum_aed")}
- Classification Weights: {compact_context.get("classification_weights")}
- Asset Type Weights: {compact_context.get("asset_type_weights")}
- Currencies (top): {compact_context.get("currencies")}

NEWS-RELEVANT HOLDINGS (FILTERED)
{holdings_text}

GENERATED INSIGHT
{insight}

TASK
Score the insight on:
1. Relevance to holdings
2. Reasoning accuracy
3. Clarity
4. Actionability

Return ONLY JSON:
{{
  "needs_revision": true,
  "score": 0-100,
  "severity": "low|medium|high",
  "issues": ["max 3 concise issue strings"],
  "rewrite_guidance": ["max 3 concise rewrite actions"],
  "full_feedback": "detailed feedback for logs"
}}
Constraints:
- Keep `issues` and `rewrite_guidance` to max 3 items each.
- Keep each issue/guidance item short and concrete.
    """
    append_insight_log(
        state.get("log_file_path"),
        event="agent_context_profile",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
            "profile": compact_profile or {},
            "prompt_char_count": len(prompt),
        },
    )
    append_insight_log(
        state.get("log_file_path"),
        event="agent_prompt_saved",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
            "prompt": prompt,
        },
    )

    result = await llm.call_text_with_usage([
        HumanMessage(content=prompt)
    ])

    usage = {
        "backend": result.backend_name,
        "provider": result.backend_provider,
        "model": result.backend_model,
        "prompt_char_count": len(prompt),
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "total_tokens": result.total_tokens,
        "raw_usage": result.raw_usage,
    }
    _record_token_usage(state, agent="verifier", usage=usage)
    append_insight_log(
        state.get("log_file_path"),
        event="agent_token_usage",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
            **usage,
        },
    )

    return _parse_verifier_output(result.text)

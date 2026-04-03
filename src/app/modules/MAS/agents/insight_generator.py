from langchain_core.messages import HumanMessage
from ..config import get_llm
from ..util.insight_logging import append_insight_log
from ..util.portfolio_compactor import (
    build_compact_portfolio_context,
    format_holdings_for_prompt,
)

llm = get_llm()


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
            "iteration": state.get("iterations", 0) + 1,
            **usage,
        }
    )


def _format_revision_guidance_for_prompt(payload: object) -> str:
    if not isinstance(payload, dict):
        return "None."
    issues = payload.get("issues") if isinstance(payload.get("issues"), list) else []
    rewrites = payload.get("rewrite_guidance") if isinstance(payload.get("rewrite_guidance"), list) else []
    if not issues and not rewrites:
        return "None."
    severity = str(payload.get("severity", "unknown")).strip().lower() or "unknown"
    lines = [f"- Severity: {severity}"]
    if issues:
        lines.append("- Issues:")
        for item in issues:
            lines.append(f"  - {str(item).strip()}")
    if rewrites:
        lines.append("- Rewrite Guidance:")
        for item in rewrites:
            lines.append(f"  - {str(item).strip()}")
    return "\n".join(lines)


async def generate_insight_agent(state: dict) -> str:
    news = state["news_document"]
    portfolio = state["client_portfolio_document"]
    revision_guidance = state.get("revision_guidance", {})
    matched_symbols = state.get("matched_tickers") or state.get("matched_isins", [])

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

    guidance_text = _format_revision_guidance_for_prompt(revision_guidance)
    holdings_text = format_holdings_for_prompt(compact_context.get("relevant_holdings", []))

    prompt = f"""
You are a financial insights assistant.

NEWS DOCUMENT
- Title: {news.get("title")}
- Teaser: {news.get("teaser")}
- Symbols: {news.get("symbols")}
- Tags: {news.get("tags")}
- Published At: {news.get("published_at")}

CLIENT PORTFOLIO SNAPSHOT
- Client Type: {compact_context.get("client_type")}
- Mandate: {compact_context.get("mandate")}
- Total AUM (aed): {compact_context.get("total_aum_aed")}
- Classification Weights: {compact_context.get("classification_weights")}
- Asset Type Weights: {compact_context.get("asset_type_weights")}
- Currencies (top): {compact_context.get("currencies")}
- Grounded Relevance: {compact_context.get("grounded_relevance")}

NEWS-RELEVANT HOLDINGS (FILTERED)
{holdings_text}

REVISION GUIDANCE (COMPACT)
{guidance_text}

TASK
Write one concise personalized insight (max 120 words) that explains:
1. Why this news matters to this portfolio
2. Likely impact
3. A practical monitoring or action cue

Rules:
- Use only provided holdings/context.
- If there is no direct holding exposure, state that and describe indirect allocation-level exposure.
- Follow revision guidance if provided. Do not repeat prior mistakes.
    """
    append_insight_log(
        state.get("log_file_path"),
        event="agent_context_profile",
        payload={
            "agent": "insight_generator",
            "iteration": state.get("iterations", 0) + 1,
            "profile": compact_profile or {},
            "prompt_char_count": len(prompt),
        },
    )
    append_insight_log(
        state.get("log_file_path"),
        event="agent_prompt_saved",
        payload={
            "agent": "insight_generator",
            "iteration": state.get("iterations", 0) + 1,
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
    _record_token_usage(state, agent="insight_generator", usage=usage)
    append_insight_log(
        state.get("log_file_path"),
        event="agent_token_usage",
        payload={
            "agent": "insight_generator",
            "iteration": state.get("iterations", 0) + 1,
            **usage,
        },
    )
    return result.text

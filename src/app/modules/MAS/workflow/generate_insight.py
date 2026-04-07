from typing import TypedDict

from langgraph.graph import END, StateGraph

from ..agents.insight_generator import generate_insight_agent
from ..agents.verifier import verify_insight_agent
from ..util.insight_logging import append_insight_log
from ..util.update_db import update_db


class InsightState(TypedDict):
    client_id: str
    news_document: dict
    client_portfolio_document: dict
    matched_tickers: list[str]
    matched_symbols: list[str]
    matched_tags: list[str]
    matched_holdings: list[dict]
    matched_holdings_count: int
    relevance_score: float
    relevance: dict
    grounded_relevance: str
    execution_route: str
    route_reason: str
    security_type_alignment: bool | None
    portfolio_snapshot: dict
    client_profile_summary: dict
    job_key: str
    log_file_path: str
    insight_draft: str
    verification_score: float
    verification_feedback: str
    verification_full_feedback: str
    revision_guidance: dict
    iterations: int
    status: str
    token_usage: dict
    compact_portfolio_context: dict
    compact_portfolio_profile: dict
    precheck_passed: bool
    precheck_reason: str
    verifier_invoked: bool


SCORE_THRESHOLD = 75.0
MAX_ITERATIONS = 3
FULL_LOOP_ROUTE = "full_loop"
SINGLE_PASS_ROUTE = "single_pass_indirect"
SKIP_ROUTE = "skip"


def _word_count(text: str) -> int:
    return len([part for part in text.split() if part.strip()])


def _has_any_direct_symbol_mention(text: str, symbols: list[str]) -> bool:
    upper_text = text.upper()
    for symbol in symbols:
        token = str(symbol or "").strip().upper()
        if token and token in upper_text:
            return True
    return False


def _compact_feedback_for_legacy(state: InsightState) -> str:
    guidance = state.get("revision_guidance") or {}
    rewrite_steps = guidance.get("rewrite_guidance", []) if isinstance(guidance, dict) else []
    if rewrite_steps:
        return " | ".join(str(step).strip() for step in rewrite_steps[:3] if str(step).strip())
    issues = guidance.get("issues", []) if isinstance(guidance, dict) else []
    if issues:
        return " | ".join(str(issue).strip() for issue in issues[:3] if str(issue).strip())
    return str(state.get("verification_full_feedback", "") or "").strip()


def _compact_payload_char_count(payload: dict) -> int:
    issues = payload.get("issues", []) if isinstance(payload.get("issues"), list) else []
    rewrites = (
        payload.get("rewrite_guidance", [])
        if isinstance(payload.get("rewrite_guidance"), list)
        else []
    )
    return len(str(payload.get("severity", ""))) + sum(
        len(str(item))
        for item in (issues + rewrites)
    )


def _route_payload(state: InsightState) -> dict:
    return {
        "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        "route_reason": state.get("route_reason", ""),
        "grounded_relevance": state.get("grounded_relevance", ""),
        "matched_holdings_count": state.get("matched_holdings_count", 0),
        "matched_symbols": state.get("matched_symbols", []),
        "security_type_alignment": state.get("security_type_alignment"),
        "verifier_invoked": state.get("verifier_invoked", False),
    }


def initialize_execution_route(state: InsightState) -> InsightState:
    route = str(state.get("execution_route") or FULL_LOOP_ROUTE).strip() or FULL_LOOP_ROUTE
    if route not in {FULL_LOOP_ROUTE, SINGLE_PASS_ROUTE, SKIP_ROUTE}:
        route = FULL_LOOP_ROUTE
    state["execution_route"] = route
    append_insight_log(
        state.get("log_file_path"),
        event="execution_route_initialized",
        payload=_route_payload(state),
    )
    return state


async def generate_insight(state: InsightState) -> InsightState:
    append_insight_log(
        state.get("log_file_path"),
        event="agent_invoked",
        payload={
            "agent": "insight_generator",
            "next_iteration": state.get("iterations", 0) + 1,
            "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        },
    )
    insight = await generate_insight_agent(state)
    state["insight_draft"] = insight
    state["iterations"] += 1
    append_insight_log(
        state.get("log_file_path"),
        event="agent_completed",
        payload={
            "agent": "insight_generator",
            "iteration": state["iterations"],
            "insight_draft": insight,
            "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        },
    )
    return state


async def precheck_insight(state: InsightState) -> InsightState:
    draft = str(state.get("insight_draft") or "").strip()
    compact_context = state.get("compact_portfolio_context") or {}
    direct_overlap = compact_context.get("news_symbol_overlap") or []
    word_count = _word_count(draft)
    lower_draft = draft.lower()

    passed = True
    reason = "passed"
    feedback = ""

    if not draft:
        passed = False
        reason = "empty_draft"
        feedback = "Draft is empty. Produce a complete insight under 120 words."
    elif not direct_overlap:
        if "no direct" not in lower_draft:
            passed = False
            reason = "missing_no_direct_exposure_statement"
            feedback = "No direct holding overlap detected. Explicitly state no direct exposure, then provide indirect allocation-level impact."
    elif not _has_any_direct_symbol_mention(draft, direct_overlap):
        passed = False
        reason = "missing_direct_symbol_reference"
        feedback = "Direct overlap exists. Mention at least one directly matched symbol/holding in the insight."

    state["precheck_passed"] = passed
    state["precheck_reason"] = reason
    if not passed:
        state["verification_score"] = 0.0
        state["verification_full_feedback"] = feedback
        state["revision_guidance"] = {
            "needs_revision": True,
            "score": 0.0,
            "severity": "high",
            "issues": [reason.replace("_", " ").strip()],
            "rewrite_guidance": [feedback],
        }
        state["verification_feedback"] = _compact_feedback_for_legacy(state)

    append_insight_log(
        state.get("log_file_path"),
        event="insight_precheck_completed",
        payload={
            "iteration": state.get("iterations", 0),
            "passed": passed,
            "reason": reason,
            "word_count": word_count,
            "direct_overlap_count": len(direct_overlap),
            "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        },
    )
    return state


async def verify_insight(state: InsightState) -> InsightState:
    state["verifier_invoked"] = True
    append_insight_log(
        state.get("log_file_path"),
        event="agent_invoked",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
            "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        },
    )
    result = await verify_insight_agent(state)
    state["verification_score"] = result["score"]
    state["verification_full_feedback"] = result["full_feedback"]
    state["revision_guidance"] = {
        "needs_revision": result["needs_revision"],
        "score": result["score"],
        "severity": result["severity"],
        "issues": result["issues"],
        "rewrite_guidance": result["rewrite_guidance"],
    }
    state["verification_feedback"] = _compact_feedback_for_legacy(state)

    full_feedback_len = len(state.get("verification_full_feedback", ""))
    compact_payload = state.get("revision_guidance", {})
    compact_payload_len = _compact_payload_char_count(compact_payload)
    compacted = full_feedback_len > compact_payload_len
    append_insight_log(
        state.get("log_file_path"),
        event="agent_completed",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
            "score": result["score"],
            "needs_revision": result["needs_revision"],
            "severity": result["severity"],
            "full_feedback": result["full_feedback"],
            "revision_guidance": compact_payload,
            "full_feedback_char_count": full_feedback_len,
            "compact_payload_char_count": compact_payload_len,
            "compaction_occurred": compacted,
            "execution_route": state.get("execution_route", FULL_LOOP_ROUTE),
        },
    )
    return state


async def _persist_insight(state: InsightState, *, status: str) -> InsightState:
    state["status"] = status
    append_insight_log(
        state.get("log_file_path"),
        event="insight_persist_started",
        payload={
            "iteration": state.get("iterations", 0),
            "status": state["status"],
            "token_usage": state.get("token_usage", {}),
            **_route_payload(state),
        },
    )
    await update_db(state)
    append_insight_log(
        state.get("log_file_path"),
        event="insight_persist_completed",
        payload={
            "iteration": state.get("iterations", 0),
            "status": state["status"],
            "token_usage": state.get("token_usage", {}),
            **_route_payload(state),
        },
    )
    return state


async def save_insight(state: InsightState) -> InsightState:
    return await _persist_insight(state, status="verified")


async def save_single_pass_insight(state: InsightState) -> InsightState:
    state["verification_feedback"] = "Verifier skipped for single_pass_indirect route."
    state["verification_full_feedback"] = state["verification_feedback"]
    state["revision_guidance"] = {
        "needs_revision": False,
        "score": 0.0,
        "severity": "low",
        "issues": [],
        "rewrite_guidance": [],
    }
    append_insight_log(
        state.get("log_file_path"),
        event="single_pass_completed",
        payload={
            "iteration": state.get("iterations", 0),
            "token_usage": state.get("token_usage", {}),
            **_route_payload(state),
        },
    )
    return await _persist_insight(state, status="single_pass_completed")


def skip_execution(state: InsightState) -> InsightState:
    state["status"] = "skipped"
    state["verification_feedback"] = state.get("route_reason", "")
    state["verification_full_feedback"] = state.get("route_reason", "")
    append_insight_log(
        state.get("log_file_path"),
        event="workflow_skipped",
        payload={
            "iteration": state.get("iterations", 0),
            "token_usage": state.get("token_usage", {}),
            **_route_payload(state),
        },
    )
    return state


def log_failure(state: InsightState) -> InsightState:
    print(
        f"[Monitor] FAILED - max iterations reached for client {state['client_id']}. "
        f"Guidance: {state.get('verification_feedback', '')}"
    )
    state["status"] = "failed"
    append_insight_log(
        state.get("log_file_path"),
        event="workflow_failed",
        payload={
            "iteration": state.get("iterations", 0),
            "feedback": state.get("verification_feedback", ""),
            "full_feedback": state.get("verification_full_feedback", ""),
            "revision_guidance": state.get("revision_guidance", {}),
            "token_usage": state.get("token_usage", {}),
            **_route_payload(state),
        },
    )
    return state


def route_at_entry(state: InsightState) -> str:
    route = str(state.get("execution_route") or FULL_LOOP_ROUTE)
    if route == SKIP_ROUTE:
        append_insight_log(
            state.get("log_file_path"),
            event="execution_route_routed",
            payload={"decision": "skip", **_route_payload(state)},
        )
        return "skip"
    append_insight_log(
        state.get("log_file_path"),
        event="execution_route_routed",
        payload={"decision": "generate", **_route_payload(state)},
    )
    return "generate"


def route_after_generation(state: InsightState) -> str:
    if state.get("execution_route") == SINGLE_PASS_ROUTE:
        append_insight_log(
            state.get("log_file_path"),
            event="generation_routed",
            payload={
                "decision": "save_single_pass",
                "iterations": state.get("iterations", 0),
                **_route_payload(state),
            },
        )
        return "save_single_pass"
    append_insight_log(
        state.get("log_file_path"),
        event="generation_routed",
        payload={
            "decision": "precheck",
            "iterations": state.get("iterations", 0),
            **_route_payload(state),
        },
    )
    return "precheck"


def route_after_verification(state: InsightState) -> str:
    if state["verification_score"] >= SCORE_THRESHOLD:
        append_insight_log(
            state.get("log_file_path"),
            event="verification_routed",
            payload={
                "decision": "save",
                "score": state["verification_score"],
                "threshold": SCORE_THRESHOLD,
                **_route_payload(state),
            },
        )
        return "save"
    if state["iterations"] >= MAX_ITERATIONS:
        append_insight_log(
            state.get("log_file_path"),
            event="verification_routed",
            payload={
                "decision": "fail",
                "score": state["verification_score"],
                "threshold": SCORE_THRESHOLD,
                "iterations": state["iterations"],
                **_route_payload(state),
            },
        )
        return "fail"
    append_insight_log(
        state.get("log_file_path"),
        event="verification_routed",
        payload={
            "decision": "regenerate",
            "score": state["verification_score"],
            "threshold": SCORE_THRESHOLD,
            "iterations": state["iterations"],
            "feedback": state.get("verification_feedback", ""),
            "revision_guidance": state.get("revision_guidance", {}),
            **_route_payload(state),
        },
    )
    return "regenerate"


def route_after_precheck(state: InsightState) -> str:
    if state.get("precheck_passed", False):
        append_insight_log(
            state.get("log_file_path"),
            event="precheck_routed",
            payload={
                "decision": "verify",
                "iterations": state.get("iterations", 0),
                **_route_payload(state),
            },
        )
        return "verify"
    if state["iterations"] >= MAX_ITERATIONS:
        append_insight_log(
            state.get("log_file_path"),
            event="precheck_routed",
            payload={
                "decision": "fail",
                "iterations": state.get("iterations", 0),
                "reason": state.get("precheck_reason", ""),
                **_route_payload(state),
            },
        )
        return "fail"
    append_insight_log(
        state.get("log_file_path"),
        event="precheck_routed",
        payload={
            "decision": "regenerate",
            "iterations": state.get("iterations", 0),
            "reason": state.get("precheck_reason", ""),
            "feedback": state.get("verification_feedback", ""),
            "revision_guidance": state.get("revision_guidance", {}),
            **_route_payload(state),
        },
    )
    return "regenerate"


def build_insight_graph() -> StateGraph:
    g = StateGraph(InsightState)
    g.add_node("initialize_route", initialize_execution_route)
    g.add_node("generate", generate_insight)
    g.add_node("precheck", precheck_insight)
    g.add_node("verify", verify_insight)
    g.add_node("save", save_insight)
    g.add_node("save_single_pass", save_single_pass_insight)
    g.add_node("skip", skip_execution)
    g.add_node("fail", log_failure)

    g.set_entry_point("initialize_route")
    g.add_conditional_edges(
        "initialize_route",
        route_at_entry,
        {
            "generate": "generate",
            "skip": "skip",
        },
    )
    g.add_conditional_edges(
        "generate",
        route_after_generation,
        {
            "precheck": "precheck",
            "save_single_pass": "save_single_pass",
        },
    )
    g.add_conditional_edges(
        "precheck",
        route_after_precheck,
        {
            "verify": "verify",
            "fail": "fail",
            "regenerate": "generate",
        },
    )
    g.add_conditional_edges(
        "verify",
        route_after_verification,
        {
            "save": "save",
            "fail": "fail",
            "regenerate": "generate",
        },
    )
    g.add_edge("save", END)
    g.add_edge("save_single_pass", END)
    g.add_edge("skip", END)
    g.add_edge("fail", END)
    return g.compile()

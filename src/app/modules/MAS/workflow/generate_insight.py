from typing import TypedDict
from langgraph.graph import StateGraph, END

from ..agents.insight_generator import generate_insight_agent
from ..agents.verifier import verify_insight_agent
from ..util.insight_logging import append_insight_log
from ..util.update_db import update_db


class InsightState(TypedDict):
    client_id: str
    news_document: dict
    client_portfolio_document: dict
    matched_isins: list[str]
    matched_tags: list[str]
    relevance_score: float
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


SCORE_THRESHOLD = 75.0
MAX_ITERATIONS = 3
MAX_DRAFT_WORDS = 130


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


async def generate_insight(state):
    append_insight_log(
        state.get("log_file_path"),
        event="agent_invoked",
        payload={
            "agent": "insight_generator",
            "next_iteration": state.get("iterations", 0) + 1,
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
        },
    )
    return state


async def precheck_insight(state):
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
    elif word_count > MAX_DRAFT_WORDS:
        passed = False
        reason = "too_long"
        feedback = "Draft is too long. Keep it under 120 words and tighten to one actionable point."
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
        },
    )
    return state


async def verify_insight(state):
    append_insight_log(
        state.get("log_file_path"),
        event="agent_invoked",
        payload={
            "agent": "verifier",
            "iteration": state.get("iterations", 0),
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
        },
    )
    return state


async def save_insight(state):
    state["status"] = "verified"
    append_insight_log(
        state.get("log_file_path"),
        event="insight_persist_started",
        payload={
            "iteration": state.get("iterations", 0),
            "status": state["status"],
            "token_usage": state.get("token_usage", {}),
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
        },
    )
    return state


def route_after_verification(state: InsightState) -> str:
    if state["verification_score"] >= SCORE_THRESHOLD:
        append_insight_log(
            state.get("log_file_path"),
            event="verification_routed",
            payload={
                "decision": "save",
                "score": state["verification_score"],
                "threshold": SCORE_THRESHOLD,
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
        },
    )
    return "regenerate"


def build_insight_graph() -> StateGraph:
    g = StateGraph(InsightState)
    g.add_node("generate", generate_insight)
    g.add_node("precheck", precheck_insight)
    g.add_node("verify", verify_insight)
    g.add_node("save", save_insight)
    g.add_node("fail", log_failure)

    g.set_entry_point("generate")
    g.add_edge("generate", "precheck")
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
    g.add_edge("fail", END)
    return g.compile()

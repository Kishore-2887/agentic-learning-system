import logging
from datetime import datetime
from app.agents.state import AgentWorkflowState
from app.providers.factory import get_llm_provider
from app.schemas import EducationalContentSchema, EvaluationResult, ImprovementResult

logger = logging.getLogger(__name__)


async def improver_agent_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Agent 4: Content Improvement Agent
    Receives evaluation critique, targets flawed or missing sections,
    remediates errors, and produces revised content.
    """
    request_id = state["request_id"]
    content_dict = state.get("current_content")
    eval_dict = state.get("latest_evaluation")
    retry_count = state.get("retry_count", 0) + 1
    state["retry_count"] = retry_count

    if not content_dict or not eval_dict:
        state["status"] = "failed"
        state["error_message"] = "Cannot improve content: content or evaluation missing."
        return state

    previous_score = eval_dict.get("overall_score", 0.0)
    logger.info(f"[{request_id}] Content Improvement Agent starting (Attempt {retry_count}). Previous score: {previous_score}")

    state["current_agent"] = "improver"
    state["status"] = "improving"
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "improver",
        "action": "improvement_started",
        "message": f"Starting refinement pass (Attempt {retry_count}/{state.get('max_retries', 3)}). Addressing feedback from score {previous_score}/100.",
        "status": "in_progress"
    })

    try:
        content = EducationalContentSchema.model_validate(content_dict)
        evaluation = EvaluationResult.model_validate(eval_dict)
        provider = get_llm_provider()

        result: ImprovementResult = await provider.improve_content(
            content=content,
            evaluation=evaluation,
            iteration=retry_count
        )

        state["current_content"] = result.revised_content.model_dump()

        # Record Revision History
        revision_entry = {
            "iteration": retry_count,
            "changes_summary": result.changelog,
            "previous_score": previous_score,
            "new_score": 0.0,  # Will be populated after re-evaluation
            "modified_sections": result.modified_sections,
            "improvements_applied": result.improvements_applied,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        state["revision_history"].append(revision_entry)

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "improver",
            "action": "improvement_completed",
            "message": f"Remediation completed for attempt {retry_count}. Modified sections: {', '.join(result.modified_sections)}. Submitting back for re-evaluation.",
            "status": "completed",
            "details": {
                "modified_sections": result.modified_sections,
                "improvements_applied": result.improvements_applied,
                "changelog": result.changelog
            }
        })
        logger.info(f"[{request_id}] Improvement pass {retry_count} completed.")
    except Exception as e:
        logger.error(f"[{request_id}] Improver Agent error: {e}", exc_info=True)
        state["status"] = "failed"
        state["error_message"] = f"Improver Agent failed: {str(e)}"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "improver",
            "action": "error",
            "message": f"Improver failed: {str(e)}",
            "status": "failed"
        })

    return state


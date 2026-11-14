import logging
from datetime import datetime
from app.agents.state import AgentWorkflowState
from app.providers.factory import get_llm_provider
from app.schemas import ContentPlan, EducationalContentSchema, FinalValidationResult

logger = logging.getLogger(__name__)


async def validator_agent_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Agent 5: Final Validation Agent
    Performs comprehensive QA audit before content is published.
    """
    request_id = state["request_id"]
    content_dict = state.get("current_content")
    plan_dict = state.get("plan")

    if not content_dict or not plan_dict:
        state["status"] = "failed"
        state["error_message"] = "Cannot validate content: content or plan is missing."
        return state

    logger.info(f"[{request_id}] Final Validation Agent starting...")

    state["current_agent"] = "validator"
    state["status"] = "validating"
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "validator",
        "action": "validation_started",
        "message": "Conducting final quality assurance, schema compliance, and requirement alignment audit.",
        "status": "in_progress"
    })

    try:
        plan = ContentPlan.model_validate(plan_dict)
        content = EducationalContentSchema.model_validate(content_dict)
        provider = get_llm_provider()

        validation: FinalValidationResult = await provider.validate_content(content, plan)

        state["final_decision"] = validation.decision
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "validator",
            "action": "validation_completed",
            "message": f"Validation decision: {validation.decision} (Confidence: {validation.confidence_score}%). {validation.summary}",
            "status": "completed",
            "details": {
                "decision": validation.decision,
                "confidence_score": validation.confidence_score,
                "factual_consistency": validation.factual_consistency_check,
                "formatting": validation.formatting_check,
                "completeness": validation.completeness_check,
                "user_alignment": validation.user_alignment_check
            }
        })

        if validation.decision == "APPROVED":
            state["status"] = "approved"
            state["is_published"] = True
        else:
            state["status"] = "manual_review"
            state["is_published"] = False

        logger.info(f"[{request_id}] Validator Agent decided: {validation.decision}")
    except Exception as e:
        logger.error(f"[{request_id}] Validator Agent error: {e}", exc_info=True)
        state["status"] = "failed"
        state["error_message"] = f"Validator Agent failed: {str(e)}"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "validator",
            "action": "error",
            "message": f"Validator failed: {str(e)}",
            "status": "failed"
        })

    return state


async def publish_approved_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Publish Approved Content Node
    Finalizes approved educational content ready for students and teachers.
    """
    request_id = state["request_id"]
    state["current_agent"] = "publisher"
    state["status"] = "completed"
    state["is_published"] = True

    latest_score = state.get("latest_evaluation", {}).get("overall_score", 0.0)
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "publisher",
        "action": "content_published",
        "message": f"Content successfully published with verified quality score of {latest_score}/100.",
        "status": "completed"
    })
    logger.info(f"[{request_id}] Content published successfully.")
    return state


async def manual_review_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Manual Review Node
    Invoked when maximum retry attempts are exhausted without reaching the threshold.
    Marks content as requiring human pedagogical review without falsely approving it.
    """
    request_id = state["request_id"]
    state["current_agent"] = "human_review"
    state["status"] = "manual_review"
    state["is_published"] = False

    latest_eval = state.get("latest_evaluation", {})
    latest_score = latest_eval.get("overall_score", 0.0)
    issues = [err.get("description", "") for err in latest_eval.get("identified_errors", [])]
    issues += latest_eval.get("missing_concepts", [])

    state["unresolved_issues"] = issues
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "supervisor",
        "action": "flagged_for_manual_review",
        "message": f"Content reached maximum retry limit ({state.get('retry_count')} attempts) with score {latest_score}/100. "
                   f"Routed to manual pedagogical review queue. Not approved for automatic publication.",
        "status": "warning",
        "details": {
            "final_score": latest_score,
            "threshold": state.get("quality_threshold"),
            "unresolved_issues": issues
        }
    })
    logger.warning(f"[{request_id}] Content flagged for manual review with score {latest_score}.")
    return state


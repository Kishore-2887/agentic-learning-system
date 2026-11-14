import logging
from datetime import datetime
from app.agents.state import AgentWorkflowState
from app.providers.factory import get_llm_provider
from app.schemas import ContentPlan, EducationalContentSchema, EvaluationResult

logger = logging.getLogger(__name__)


async def evaluator_agent_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Agent 3: Quality Evaluator Agent
    Rigorous independent scoring across 6 weighted dimensions.
    Flags unsupported claims, factual issues, and concept omissions.
    """
    request_id = state["request_id"]
    content_dict = state.get("current_content")
    plan_dict = state.get("plan")
    threshold = state.get("quality_threshold", 80.0)
    retry_count = state.get("retry_count", 0)

    if not content_dict or not plan_dict:
        state["status"] = "failed"
        state["error_message"] = "Cannot evaluate content: content or plan is missing."
        return state

    logger.info(f"[{request_id}] Quality Evaluator Agent running (Iteration {retry_count + 1})...")

    state["current_agent"] = "evaluator"
    state["status"] = "evaluating"
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "evaluator",
        "action": "evaluation_started",
        "message": f"Conducting multi-dimensional quality & factual evaluation (Iteration {retry_count + 1}, Threshold: {threshold}/100).",
        "status": "in_progress"
    })

    try:
        plan = ContentPlan.model_validate(plan_dict)
        content = EducationalContentSchema.model_validate(content_dict)
        provider = get_llm_provider()

        evaluation: EvaluationResult = await provider.evaluate_content(
            content=content,
            plan=plan,
            quality_threshold=threshold
        )

        eval_dict = evaluation.model_dump()
        state["latest_evaluation"] = eval_dict

        status_flag = "PASSED" if evaluation.passed else "NEEDS_IMPROVEMENT"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "evaluator",
            "action": "evaluation_completed",
            "message": f"Evaluation finished: Score {evaluation.overall_score}/100 [{status_flag}]. "
                       f"Identified {len(evaluation.identified_errors)} errors, {len(evaluation.missing_concepts)} missing concepts, {len(evaluation.unsupported_claims)} unsupported claims.",
            "status": "completed",
            "details": {
                "overall_score": evaluation.overall_score,
                "passed": evaluation.passed,
                "factual_accuracy": evaluation.factual_accuracy,
                "relevance": evaluation.relevance,
                "completeness": evaluation.completeness,
                "clarity_readability": evaluation.clarity_readability,
                "educational_effectiveness": evaluation.educational_effectiveness,
                "structure_organization": evaluation.structure_organization,
                "errors_count": len(evaluation.identified_errors),
                "missing_concepts_count": len(evaluation.missing_concepts),
                "unsupported_claims_count": len(evaluation.unsupported_claims)
            }
        })
        logger.info(f"[{request_id}] Evaluator Agent finished with score {evaluation.overall_score} (passed={evaluation.passed}).")
    except Exception as e:
        logger.error(f"[{request_id}] Evaluator Agent error: {e}", exc_info=True)
        state["status"] = "failed"
        state["error_message"] = f"Evaluator Agent failed: {str(e)}"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "evaluator",
            "action": "error",
            "message": f"Evaluator failed: {str(e)}",
            "status": "failed"
        })

    return state


import logging
from datetime import datetime
from app.agents.state import AgentWorkflowState
from app.providers.factory import get_llm_provider
from app.schemas import ContentPlan

logger = logging.getLogger(__name__)


async def planner_agent_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Agent 1: Content Planner Agent
    Analyzes topic, target audience, education level, learning objectives,
    and produces a structured instructional outline and evaluation criteria.
    """
    request_id = state["request_id"]
    topic = state["topic"]
    audience = state["target_audience"]
    edu_level = state["education_level"]
    objectives = state["learning_objectives"]
    content_type = state["content_type"]

    logger.info(f"[{request_id}] Planner Agent starting for topic: '{topic}'")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "planner",
        "action": "planning_started",
        "message": f"Analyzing pedagogical requirements for '{topic}' targeted at {audience} ({edu_level}).",
        "status": "in_progress"
    }
    state["logs"].append(log_entry)
    state["current_agent"] = "planner"
    state["status"] = "planning"

    try:
        provider = get_llm_provider()
        plan: ContentPlan = await provider.generate_plan(
            topic=topic,
            target_audience=audience,
            education_level=edu_level,
            learning_objectives=objectives,
            content_type=content_type
        )

        state["plan"] = plan.model_dump()
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "planner",
            "action": "plan_created",
            "message": f"Instructional blueprint constructed with {len(plan.outline)} modules and {len(plan.evaluation_criteria)} evaluation criteria.",
            "status": "completed",
            "details": {
                "modules_count": len(plan.outline),
                "criteria": plan.evaluation_criteria
            }
        })
        logger.info(f"[{request_id}] Planner Agent completed successfully.")
    except Exception as e:
        logger.error(f"[{request_id}] Planner Agent error: {e}", exc_info=True)
        state["status"] = "failed"
        state["error_message"] = f"Planner Agent failed: {str(e)}"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "planner",
            "action": "error",
            "message": f"Planner failed: {str(e)}",
            "status": "failed"
        })

    return state


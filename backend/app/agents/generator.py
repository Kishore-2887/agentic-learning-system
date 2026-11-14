import logging
from datetime import datetime
from app.agents.state import AgentWorkflowState
from app.providers.factory import get_llm_provider
from app.schemas import ContentPlan, EducationalContentSchema

logger = logging.getLogger(__name__)


async def generator_agent_node(state: AgentWorkflowState) -> AgentWorkflowState:
    """
    Agent 2: Content Generator Agent
    Synthesizes educational content based on the approved instructional plan.
    """
    request_id = state["request_id"]
    plan_dict = state.get("plan")

    if not plan_dict:
        state["status"] = "failed"
        state["error_message"] = "Cannot generate content without an approved plan."
        return state

    logger.info(f"[{request_id}] Generator Agent generating content...")

    state["current_agent"] = "generator"
    state["status"] = "generating"
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "generator",
        "action": "generation_started",
        "message": f"Drafting full curriculum content for '{state['topic']}' across {len(plan_dict.get('outline', []))} planned sections.",
        "status": "in_progress"
    })

    try:
        plan = ContentPlan.model_validate(plan_dict)
        provider = get_llm_provider()
        content: EducationalContentSchema = await provider.generate_content(plan)

        content_dict = content.model_dump()
        state["current_content"] = content_dict

        total_words = sum(len(sec["explanation"].split()) for sec in content_dict["sections"])
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "generator",
            "action": "content_generated",
            "message": f"Initial educational draft generated ({len(content_dict['sections'])} sections, {len(content_dict['practice_questions'])} practice questions, ~{total_words} words).",
            "status": "completed",
            "details": {
                "title": content_dict["title"],
                "section_count": len(content_dict["sections"]),
                "questions_count": len(content_dict["practice_questions"]),
                "estimated_words": total_words
            }
        })
        logger.info(f"[{request_id}] Generator Agent completed successfully.")
    except Exception as e:
        logger.error(f"[{request_id}] Generator Agent error: {e}", exc_info=True)
        state["status"] = "failed"
        state["error_message"] = f"Generator Agent failed: {str(e)}"
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "generator",
            "action": "error",
            "message": f"Generator failed: {str(e)}",
            "status": "failed"
        })

    return state


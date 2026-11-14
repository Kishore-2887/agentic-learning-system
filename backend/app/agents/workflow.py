import logging
from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentWorkflowState
from app.agents.planner import planner_agent_node
from app.agents.generator import generator_agent_node
from app.agents.evaluator import evaluator_agent_node
from app.agents.improver import improver_agent_node
from app.agents.validator import (
    validator_agent_node,
    publish_approved_node,
    manual_review_node
)

logger = logging.getLogger(__name__)


def decision_router(state: AgentWorkflowState) -> str:
    """
    Conditional routing logic after evaluation:
    - If score >= threshold: route to Final Validation Agent.
    - If score < threshold and retry_count < max_retries: route to Improvement Agent.
    - If score < threshold and retry_count >= max_retries: route to Manual Review.
    """
    eval_dict = state.get("latest_evaluation") or {}
    score = eval_dict.get("overall_score", 0.0)
    threshold = state.get("quality_threshold", 80.0)
    passed = eval_dict.get("passed", False) or (score >= threshold)
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if passed:
        logger.info(f"[{state['request_id']}] Quality score {score} >= {threshold}. Routing to validator.")
        return "validator"

    if retry_count < max_retries:
        logger.info(f"[{state['request_id']}] Quality score {score} < {threshold}. Routing to improver (Attempt {retry_count + 1}/{max_retries}).")
        return "improver"

    logger.warning(f"[{state['request_id']}] Max retries ({max_retries}) reached with score {score}. Routing to manual review.")
    return "manual_review"


def validation_router(state: AgentWorkflowState) -> str:
    """
    Routes validator output to either publication or manual review.
    """
    decision = state.get("final_decision", "REJECTED")
    if decision == "APPROVED":
        return "publish"
    return "manual_review"


def create_learning_content_graph():
    """
    Builds and compiles the full LangGraph state machine workflow.
    """
    workflow = StateGraph(AgentWorkflowState)

    # 1. Add specialized agent nodes
    workflow.add_node("planner", planner_agent_node)
    workflow.add_node("generator", generator_agent_node)
    workflow.add_node("evaluator", evaluator_agent_node)
    workflow.add_node("improver", improver_agent_node)
    workflow.add_node("validator", validator_agent_node)
    workflow.add_node("publish", publish_approved_node)
    workflow.add_node("manual_review", manual_review_node)

    # 2. Add fixed sequential edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "evaluator")

    # 3. Add conditional edge from evaluator
    workflow.add_conditional_edges(
        "evaluator",
        decision_router,
        {
            "validator": "validator",
            "improver": "improver",
            "manual_review": "manual_review"
        }
    )

    # 4. Improver loops back into evaluator
    workflow.add_edge("improver", "evaluator")

    # 5. Validator routes to publish or manual review
    workflow.add_conditional_edges(
        "validator",
        validation_router,
        {
            "publish": "publish",
            "manual_review": "manual_review"
        }
    )

    # 6. Terminal edges
    workflow.add_edge("publish", END)
    workflow.add_edge("manual_review", END)

    return workflow.compile()


# Pre-compiled workflow graph instance
learning_content_graph = create_learning_content_graph()


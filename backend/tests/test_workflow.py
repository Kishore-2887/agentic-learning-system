import pytest
from app.agents.workflow import create_learning_content_graph
from app.agents.state import AgentWorkflowState


@pytest.mark.asyncio
async def test_full_langgraph_workflow_loop():
    graph = create_learning_content_graph()

    initial_state: AgentWorkflowState = {
        "request_id": "test-req-001",
        "topic": "Distributed Consensus Algorithms",
        "target_audience": "Systems Engineers",
        "education_level": "Advanced",
        "learning_objectives": ["Understand Raft vs Paxos", "Explain Leader Election"],
        "content_type": "tutorial",
        "quality_threshold": 80.0,
        "max_retries": 3,
        "retry_count": 0,
        "plan": None,
        "current_content": None,
        "latest_evaluation": None,
        "revision_history": [],
        "status": "running",
        "current_agent": "planner",
        "logs": [],
        "unresolved_issues": [],
        "final_decision": None,
        "is_published": False,
        "content_id": None,
        "error_message": None
    }

    final_state = await graph.ainvoke(initial_state)

    # Assertions
    assert final_state["plan"] is not None
    assert final_state["current_content"] is not None
    assert final_state["latest_evaluation"] is not None
    # Verify it went through the loop: evaluated -> improved -> re-evaluated -> validated
    assert final_state["retry_count"] >= 1
    assert len(final_state["revision_history"]) >= 1
    assert final_state["latest_evaluation"]["overall_score"] >= 80.0
    assert final_state["final_decision"] == "APPROVED"
    assert final_state["is_published"] is True
    assert final_state["status"] == "completed"


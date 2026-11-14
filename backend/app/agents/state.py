from typing import TypedDict, List, Dict, Any, Optional


class AgentWorkflowState(TypedDict):
    request_id: str
    topic: str
    target_audience: str
    education_level: str
    learning_objectives: List[str]
    content_type: str
    quality_threshold: float
    max_retries: int
    retry_count: int

    # Agent Artifacts
    plan: Optional[Dict[str, Any]]
    current_content: Optional[Dict[str, Any]]
    latest_evaluation: Optional[Dict[str, Any]]
    revision_history: List[Dict[str, Any]]

    # Workflow Orchestration
    status: str  # "pending", "planning", "generating", "evaluating", "improving", "validating", "approved", "manual_review", "failed"
    current_agent: str
    logs: List[Dict[str, Any]]
    unresolved_issues: List[str]
    final_decision: Optional[str]
    is_published: bool
    content_id: Optional[str]
    error_message: Optional[str]


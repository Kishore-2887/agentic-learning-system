from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# --- Rubric Hard Pass/Fail Checkpoints ---

class RubricCheckpoint(BaseModel):
    name: str  # e.g., "accurate_and_grounded", "beginner_friendly_language", "teaches_by_example", "no_unexplained_jargon", "covers_key_points", "coherent_teaching_flow"
    label: str
    passed: bool
    reason: str


class RejectionLogItem(BaseModel):
    iteration: int
    failed_checkpoints: List[str]
    critique: str
    changes_made_on_retry: str
    timestamp: str


# --- Agent Structured Output Schemas ---

class PlanSection(BaseModel):
    title: str
    subtopics: List[str]
    target_learning_outcome: str


class ContentPlan(BaseModel):
    topic: str
    target_audience: str
    education_level: str
    learning_objectives: List[str]
    difficulty_level: str
    outline: List[PlanSection]
    evaluation_criteria: List[str]
    analogy_selected: Optional[str] = None  # e.g., "Open-Book vs Closed-Book Exam"


class PracticeQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = None
    answer: str
    explanation: str


class ContentSection(BaseModel):
    title: str
    explanation: str
    examples: List[str] = Field(default_factory=list)
    callout_note: Optional[str] = None
    key_terms: List[str] = Field(default_factory=list)


class EducationalContentSchema(BaseModel):
    title: str
    topic: str
    target_audience: str
    education_level: str
    summary: str
    core_analogy: str  # Relatable real-world analogy
    key_concepts: List[str]
    sections: List[ContentSection]
    practice_questions: List[PracticeQuestion]
    key_takeaways: List[str]
    references_and_further_reading: List[str] = Field(default_factory=list)


class IdentifiedError(BaseModel):
    section: str
    severity: str  # "minor", "moderate", "critical"
    description: str
    unsupported_claim: bool = False


class EvaluationResult(BaseModel):
    # 6 Hard Pass/Fail Checkpoints (No partial credit)
    checkpoints: List[RubricCheckpoint] = Field(default_factory=list)
    all_checkpoints_passed: bool = False

    # Weighted Dimension Scores for granular analytics
    factual_accuracy: float = Field(..., ge=0, le=100)
    relevance: float = Field(..., ge=0, le=100)
    completeness: float = Field(..., ge=0, le=100)
    clarity_readability: float = Field(..., ge=0, le=100)
    educational_effectiveness: float = Field(..., ge=0, le=100)
    structure_organization: float = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)
    passed: bool

    identified_errors: List[IdentifiedError] = Field(default_factory=list)
    missing_concepts: List[str] = Field(default_factory=list)
    improvement_recommendations: List[str] = Field(default_factory=list)
    unsupported_claims: List[str] = Field(default_factory=list)


class ImprovementResult(BaseModel):
    revised_content: EducationalContentSchema
    changelog: str
    modified_sections: List[str]
    improvements_applied: List[str]
    rejection_resolution_summary: str


class FinalValidationResult(BaseModel):
    passed: bool
    decision: str  # "APPROVED" or "REJECTED"
    factual_consistency_check: bool
    formatting_check: bool
    completeness_check: bool
    user_alignment_check: bool
    confidence_score: float = Field(default=95.0, ge=0, le=100)
    summary: str


# --- API Request & Response Schemas ---

class ContentGenerateRequest(BaseModel):
    topic: str = Field(default="Introduction to RAG (Retrieval-Augmented Generation)")
    target_audience: str = Field(default="12th-grade graduate from India, limited English vocabulary, non-English-medium background, aspiring AI career")
    education_level: str = Field(default="Beginner / 12th Grade")
    learning_objectives: List[str] = Field(default_factory=list)
    content_type: str = Field(default="lesson")
    quality_threshold: Optional[float] = Field(default=80.0, ge=50, le=100)
    max_retries: Optional[int] = Field(default=2, ge=1, le=3)
    inject_deliberate_flaw: Optional[bool] = Field(default=False, description="Deliberately injects a flaw on pass 1 to demonstrate evaluator error catching for Loom demo video")


class EvaluationReportResponse(BaseModel):
    id: str
    iteration: int
    all_checkpoints_passed: bool
    checkpoints: List[Dict[str, Any]]
    factual_accuracy: float
    relevance: float
    completeness: float
    clarity_readability: float
    educational_effectiveness: float
    structure_organization: float
    overall_score: float
    passed: bool
    identified_errors: List[Dict[str, Any]]
    missing_concepts: List[str]
    improvement_recommendations: List[str]
    unsupported_claims: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RevisionHistoryResponse(BaseModel):
    id: str
    iteration: int
    changes_summary: str
    previous_score: float
    new_score: float
    modified_sections: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentResponse(BaseModel):
    id: str
    request_id: str
    version: int
    title: str
    raw_json: Dict[str, Any]
    markdown_text: str
    word_count: int
    is_published: bool
    status: str
    created_at: datetime
    latest_evaluation: Optional[EvaluationReportResponse] = None
    rejection_log: List[RejectionLogItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ContentListItem(BaseModel):
    id: str
    request_id: str
    title: str
    topic: str
    education_level: str
    version: int
    status: str
    is_published: bool
    overall_score: Optional[float] = None
    all_checkpoints_passed: Optional[bool] = None
    created_at: datetime


class WorkflowLogItem(BaseModel):
    timestamp: str
    agent: str
    action: str
    message: str
    status: str
    details: Optional[Dict[str, Any]] = None


class WorkflowStatusResponse(BaseModel):
    request_id: str
    status: str
    current_agent: str
    retry_count: int
    max_retries: int
    quality_threshold: float
    latest_score: Optional[float] = None
    passed: Optional[bool] = None
    all_checkpoints_passed: Optional[bool] = None
    checkpoints: List[Dict[str, Any]] = Field(default_factory=list)
    rejection_log: List[RejectionLogItem] = Field(default_factory=list)
    logs: List[WorkflowLogItem] = Field(default_factory=list)
    content_id: Optional[str] = None
    unresolved_issues: List[str] = Field(default_factory=list)
    final_decision: Optional[str] = None


class AnalyticsResponse(BaseModel):
    total_generated: int
    approved_count: int
    manual_review_count: int
    failed_count: int
    average_quality_score: float
    pass_rate_percentage: float
    dimension_averages: Dict[str, float]
    score_distribution: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
    learned_rules_count: int = 0


class SettingsResponse(BaseModel):
    llm_provider: str
    available_providers: List[str]
    openai_model: str
    gemini_model: str
    default_quality_threshold: float
    max_improvement_attempts: int
    openai_key_configured: bool
    gemini_key_configured: bool
    persistent_memory_enabled: bool = True
    learned_rules: List[str] = Field(default_factory=list)


class SettingsUpdateRequest(BaseModel):
    llm_provider: Optional[str] = None
    openai_model: Optional[str] = None
    gemini_model: Optional[str] = None
    default_quality_threshold: Optional[float] = None
    max_improvement_attempts: Optional[int] = None

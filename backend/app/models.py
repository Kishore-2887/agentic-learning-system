import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ContentRequest(Base):
    __tablename__ = "content_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    topic = Column(String(255), nullable=False)
    target_audience = Column(String(255), nullable=False)
    education_level = Column(String(100), nullable=False)
    learning_objectives = Column(JSON, nullable=False, default=list)
    content_type = Column(String(100), nullable=False, default="lesson")
    quality_threshold = Column(Float, default=80.0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, failed, manual_review

    # Relationships
    contents = relationship("GeneratedContent", back_populates="request", cascade="all, delete-orphan")
    evaluations = relationship("EvaluationReport", back_populates="request", cascade="all, delete-orphan")
    revisions = relationship("RevisionHistory", back_populates="request", cascade="all, delete-orphan")
    executions = relationship("WorkflowExecution", back_populates="request", cascade="all, delete-orphan")


class GeneratedContent(Base):
    __tablename__ = "generated_content"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("content_requests.id"), nullable=False)
    version = Column(Integer, default=1)
    title = Column(String(255), nullable=False)
    raw_json = Column(JSON, nullable=False)  # Full structured educational content JSON
    markdown_text = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    status = Column(String(50), default="draft")  # draft, approved, rejected, manual_review
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    request = relationship("ContentRequest", back_populates="contents")
    evaluations = relationship("EvaluationReport", back_populates="content", cascade="all, delete-orphan")


class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("content_requests.id"), nullable=False)
    content_id = Column(String(36), ForeignKey("generated_content.id"), nullable=True)
    iteration = Column(Integer, default=1)

    # 6 weighted evaluation dimensions:
    factual_accuracy = Column(Float, nullable=False)       # 25%
    relevance = Column(Float, nullable=False)              # 20%
    completeness = Column(Float, nullable=False)           # 20%
    clarity_readability = Column(Float, nullable=False)    # 15%
    educational_effectiveness = Column(Float, nullable=False) # 10%
    structure_organization = Column(Float, nullable=False) # 10%

    overall_score = Column(Float, nullable=False)
    passed = Column(Boolean, default=False)

    identified_errors = Column(JSON, default=list)       # List of error objects
    missing_concepts = Column(JSON, default=list)        # List of missing concept strings
    improvement_recommendations = Column(JSON, default=list) # Recommendations list
    unsupported_claims = Column(JSON, default=list)      # Flagged claims without verification

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    request = relationship("ContentRequest", back_populates="evaluations")
    content = relationship("GeneratedContent", back_populates="evaluations")


class RevisionHistory(Base):
    __tablename__ = "revision_history"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("content_requests.id"), nullable=False)
    iteration = Column(Integer, default=1)
    changes_summary = Column(Text, nullable=False)
    previous_score = Column(Float, default=0.0)
    new_score = Column(Float, default=0.0)
    modified_sections = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    request = relationship("ContentRequest", back_populates="revisions")


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("content_requests.id"), nullable=False)
    current_agent = Column(String(100), default="planner")
    status = Column(String(50), default="running")  # running, completed, manual_review, failed
    retry_count = Column(Integer, default=0)
    logs = Column(JSON, default=list)  # List of log event dicts
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationship
    request = relationship("ContentRequest", back_populates="executions")


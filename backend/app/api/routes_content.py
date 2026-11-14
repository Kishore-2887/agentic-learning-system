import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ContentRequest, GeneratedContent, EvaluationReport, RevisionHistory
from app.schemas import (
    ContentGenerateRequest,
    ContentResponse,
    ContentListItem,
    EvaluationReportResponse,
    RevisionHistoryResponse
)
from app.services.workflow_runner import execute_content_generation_workflow

router = APIRouter(prefix="/api/content", tags=["Content"])
logger = logging.getLogger(__name__)


@router.post("/generate", status_code=202)
def generate_content(
    payload: ContentGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submits a new educational content generation and self-evaluation request.
    Initializes a multi-agent LangGraph workflow running asynchronously.
    """
    new_request = ContentRequest(
        topic=payload.topic.strip(),
        target_audience=payload.target_audience.strip(),
        education_level=payload.education_level.strip(),
        learning_objectives=payload.learning_objectives or [],
        content_type=payload.content_type,
        quality_threshold=payload.quality_threshold or 80.0,
        max_retries=payload.max_retries or 3,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # Launch background agent workflow
    background_tasks.add_task(
        execute_content_generation_workflow,
        request_id=new_request.id,
        topic=new_request.topic,
        target_audience=new_request.target_audience,
        education_level=new_request.education_level,
        learning_objectives=new_request.learning_objectives,
        content_type=new_request.content_type,
        quality_threshold=new_request.quality_threshold,
        max_retries=new_request.max_retries
    )

    return {
        "request_id": new_request.id,
        "status": "pending",
        "message": f"Agent workflow scheduled for '{new_request.topic}'."
    }


@router.get("", response_model=List[ContentListItem])
def list_content(
    search: Optional[str] = Query(None, description="Search query by topic or title"),
    status: Optional[str] = Query(None, description="Filter by status (approved, manual_review, draft)"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieves all generated learning content items with latest score & publication status.
    """
    query = db.query(GeneratedContent).join(ContentRequest, GeneratedContent.request_id == ContentRequest.id)

    if search:
        query = query.filter(
            (GeneratedContent.title.ilike(f"%{search}%")) |
            (ContentRequest.topic.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter(GeneratedContent.status == status)

    contents = query.order_by(GeneratedContent.created_at.desc()).offset(skip).limit(limit).all()

    items = []
    for c in contents:
        # Get latest evaluation score
        latest_eval = db.query(EvaluationReport).filter(
            EvaluationReport.content_id == c.id
        ).order_by(EvaluationReport.iteration.desc()).first()

        items.append(ContentListItem(
            id=c.id,
            request_id=c.request_id,
            title=c.title,
            topic=c.request.topic if c.request else c.title,
            education_level=c.request.education_level if c.request else "General",
            version=c.version,
            status=c.status,
            is_published=c.is_published,
            overall_score=latest_eval.overall_score if latest_eval else None,
            created_at=c.created_at
        ))

    return items


@router.get("/{id}", response_model=ContentResponse)
def get_content_detail(id: str, db: Session = Depends(get_db)):
    """
    Retrieves complete educational content details including raw JSON, Markdown, and latest evaluation.
    """
    content = db.query(GeneratedContent).filter(GeneratedContent.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail=f"Content with id '{id}' not found.")

    latest_eval = db.query(EvaluationReport).filter(
        EvaluationReport.content_id == content.id
    ).order_by(EvaluationReport.iteration.desc()).first()

    return ContentResponse(
        id=content.id,
        request_id=content.request_id,
        version=content.version,
        title=content.title,
        raw_json=content.raw_json,
        markdown_text=content.markdown_text,
        word_count=content.word_count,
        is_published=content.is_published,
        status=content.status,
        created_at=content.created_at,
        latest_evaluation=latest_eval
    )


@router.get("/{id}/evaluation", response_model=List[EvaluationReportResponse])
def get_content_evaluations(id: str, db: Session = Depends(get_db)):
    """
    Retrieves all evaluation iterations and detailed score breakdowns for content id or request id.
    """
    # Check if id matches content_id or request_id
    evals = db.query(EvaluationReport).filter(
        (EvaluationReport.content_id == id) | (EvaluationReport.request_id == id)
    ).order_by(EvaluationReport.iteration.asc()).all()

    if not evals:
        # Check if content exists
        content = db.query(GeneratedContent).filter(GeneratedContent.id == id).first()
        if content:
            evals = db.query(EvaluationReport).filter(
                EvaluationReport.request_id == content.request_id
            ).order_by(EvaluationReport.iteration.asc()).all()

    return evals


@router.get("/{id}/history", response_model=List[RevisionHistoryResponse])
def get_content_history(id: str, db: Session = Depends(get_db)):
    """
    Retrieves the revision and remediation history for this content.
    """
    content = db.query(GeneratedContent).filter(GeneratedContent.id == id).first()
    request_id = content.request_id if content else id

    revisions = db.query(RevisionHistory).filter(
        RevisionHistory.request_id == request_id
    ).order_by(RevisionHistory.iteration.asc()).all()

    return revisions


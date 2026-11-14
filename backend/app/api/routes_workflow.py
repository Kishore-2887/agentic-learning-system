import asyncio
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ContentRequest, WorkflowExecution, EvaluationReport, GeneratedContent, RevisionHistory
from app.schemas import WorkflowStatusResponse
from app.services.workflow_runner import get_workflow_state, ACTIVE_WORKFLOWS

router = APIRouter(prefix="/api/workflow", tags=["Workflow"])
logger = logging.getLogger(__name__)


@router.get("/{id}/status", response_model=WorkflowStatusResponse)
def get_workflow_status(id: str, db: Session = Depends(get_db)):
    # 1. Check in-memory active cache
    active = get_workflow_state(id)
    if active:
        latest_eval = active.get("latest_evaluation") or {}
        return WorkflowStatusResponse(
            request_id=id,
            status=active.get("status", "running"),
            current_agent=active.get("current_agent", "planner"),
            retry_count=active.get("retry_count", 0),
            max_retries=active.get("max_retries", 2),
            quality_threshold=active.get("quality_threshold", 80.0),
            latest_score=latest_eval.get("overall_score"),
            passed=latest_eval.get("passed"),
            all_checkpoints_passed=latest_eval.get("all_checkpoints_passed"),
            checkpoints=latest_eval.get("checkpoints", []),
            rejection_log=active.get("rejection_log", []),
            logs=active.get("logs", []),
            content_id=active.get("content_id"),
            unresolved_issues=active.get("unresolved_issues", []),
            final_decision=active.get("final_decision")
        )

    # 2. Check Database
    execution = db.query(WorkflowExecution).filter(WorkflowExecution.request_id == id).first()
    request_rec = db.query(ContentRequest).filter(ContentRequest.id == id).first()

    if not request_rec and not execution:
        raise HTTPException(status_code=404, detail=f"Workflow with ID '{id}' not found.")

    latest_eval = db.query(EvaluationReport).filter(
        EvaluationReport.request_id == id
    ).order_by(EvaluationReport.iteration.desc()).first()

    content = db.query(GeneratedContent).filter(GeneratedContent.request_id == id).first()
    revisions = db.query(RevisionHistory).filter(RevisionHistory.request_id == id).all()

    # Reconstruct rejection log from revision history
    reconstructed_rejections = []
    for r in revisions:
        reconstructed_rejections.append({
            "iteration": r.iteration,
            "failed_checkpoints": ["Remediated Checkpoints"],
            "critique": f"Previous Score: {r.previous_score}/100",
            "changes_made_on_retry": r.changes_summary,
            "timestamp": r.created_at.isoformat()
        })

    return WorkflowStatusResponse(
        request_id=id,
        status=execution.status if execution else (request_rec.status if request_rec else "completed"),
        current_agent=execution.current_agent if execution else "publisher",
        retry_count=execution.retry_count if execution else 0,
        max_retries=request_rec.max_retries if request_rec else 2,
        quality_threshold=request_rec.quality_threshold if request_rec else 80.0,
        latest_score=latest_eval.overall_score if latest_eval else None,
        passed=latest_eval.passed if latest_eval else None,
        all_checkpoints_passed=latest_eval.passed if latest_eval else None,
        checkpoints=[],
        rejection_log=reconstructed_rejections,
        logs=execution.logs if execution and execution.logs else [],
        content_id=content.id if content else None,
        unresolved_issues=[],
        final_decision="APPROVED" if (content and content.is_published) else None
    )


@router.get("/{id}/stream")
async def stream_workflow_progress(id: str):
    async def event_generator():
        last_log_count = 0
        terminal_states = {"completed", "manual_review", "failed"}

        for _ in range(120):
            state = get_workflow_state(id)

            if state:
                status = state.get("status", "running")
                logs = state.get("logs", [])
                latest_eval = state.get("latest_evaluation") or {}

                payload = {
                    "request_id": id,
                    "status": status,
                    "current_agent": state.get("current_agent", "planner"),
                    "retry_count": state.get("retry_count", 0),
                    "quality_threshold": state.get("quality_threshold", 80.0),
                    "latest_score": latest_eval.get("overall_score"),
                    "passed": latest_eval.get("passed"),
                    "all_checkpoints_passed": latest_eval.get("all_checkpoints_passed"),
                    "checkpoints": latest_eval.get("checkpoints", []),
                    "rejection_log": state.get("rejection_log", []),
                    "content_id": state.get("content_id"),
                    "new_logs": logs[last_log_count:],
                    "final_decision": state.get("final_decision")
                }
                last_log_count = len(logs)

                yield f"data: {json.dumps(payload)}\n\n"

                if status in terminal_states:
                    break
            else:
                yield f"data: {json.dumps({'request_id': id, 'status': 'waiting', 'current_agent': 'queue'})}\n\n"

            await asyncio.sleep(1.0)

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    ContentRequest,
    GeneratedContent,
    EvaluationReport,
    RevisionHistory,
    WorkflowExecution
)
from app.agents.state import AgentWorkflowState
from app.agents.workflow import learning_content_graph
from app.utils.markdown_export import content_to_markdown

logger = logging.getLogger(__name__)

ACTIVE_WORKFLOWS: Dict[str, Dict[str, Any]] = {}


def get_workflow_state(request_id: str) -> Optional[Dict[str, Any]]:
    return ACTIVE_WORKFLOWS.get(request_id)


async def execute_content_generation_workflow(
    request_id: str,
    topic: str,
    target_audience: str,
    education_level: str,
    learning_objectives: list,
    content_type: str,
    quality_threshold: float,
    max_retries: int,
    inject_deliberate_flaw: bool = False
):
    logger.info(f"Starting workflow execution for request_id: {request_id}")

    utc_now = datetime.now(timezone.utc)

    initial_state: AgentWorkflowState = {
        "request_id": request_id,
        "topic": topic,
        "target_audience": target_audience,
        "education_level": education_level,
        "learning_objectives": learning_objectives,
        "content_type": content_type,
        "quality_threshold": quality_threshold,
        "max_retries": max_retries,
        "retry_count": 0,
        "plan": None,
        "current_content": None,
        "latest_evaluation": None,
        "revision_history": [],
        "status": "running",
        "current_agent": "planner",
        "logs": [
            {
                "timestamp": utc_now.isoformat(),
                "agent": "orchestrator",
                "action": "workflow_initialized",
                "message": f"Multi-Agent LangGraph workflow initialized for topic: '{topic}'.",
                "status": "in_progress"
            }
        ],
        "unresolved_issues": [],
        "final_decision": None,
        "is_published": False,
        "content_id": None,
        "error_message": None
    }

    # Tracking rejection log in active state
    initial_state["rejection_log"] = []
    ACTIVE_WORKFLOWS[request_id] = initial_state

    # DB Init
    db: Session = SessionLocal()
    try:
        execution = WorkflowExecution(
            request_id=request_id,
            current_agent="planner",
            status="running",
            retry_count=0,
            logs=initial_state["logs"],
            started_at=datetime.utcnow()
        )
        db.add(execution)
        req = db.query(ContentRequest).filter(ContentRequest.id == request_id).first()
        if req:
            req.status = "in_progress"
        db.commit()
    except Exception as e:
        logger.error(f"Error initializing DB execution record: {e}")
    finally:
        db.close()

    final_state = initial_state
    try:
        async for chunk in learning_content_graph.astream(initial_state):
            for node_name, updated_state in chunk.items():
                logger.info(f"Workflow reached node: {node_name}")
                final_state = updated_state

                # Check if evaluator caught an issue and create rejection log entry
                latest_eval = final_state.get("latest_evaluation") or {}
                checkpoints = latest_eval.get("checkpoints", [])
                failed_checkpoints = [cp.get("label") for cp in checkpoints if not cp.get("passed")]

                if failed_checkpoints and node_name == "evaluator":
                    rejection_item = {
                        "iteration": final_state.get("retry_count", 0) + 1,
                        "failed_checkpoints": failed_checkpoints,
                        "critique": f"Quality Gate Rejected: Failed [{', '.join(failed_checkpoints)}].",
                        "changes_made_on_retry": "Pending remediation by Content Improvement Agent...",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    if "rejection_log" not in final_state:
                        final_state["rejection_log"] = []
                    # Append if not duplicate for this iteration
                    if not any(r["iteration"] == rejection_item["iteration"] for r in final_state["rejection_log"]):
                        final_state["rejection_log"].append(rejection_item)

                if node_name == "improver" and final_state.get("rejection_log"):
                    # Update the latest rejection log entry with the changes applied
                    revs = final_state.get("revision_history", [])
                    if revs:
                        latest_rev = revs[-1]
                        final_state["rejection_log"][-1]["changes_made_on_retry"] = latest_rev.get("changes_summary", "")

                ACTIVE_WORKFLOWS[request_id] = final_state

                # Checkpoint DB
                db = SessionLocal()
                try:
                    exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.request_id == request_id).first()
                    if exec_record:
                        exec_record.current_agent = final_state.get("current_agent", node_name)
                        exec_record.status = final_state.get("status", "running")
                        exec_record.retry_count = final_state.get("retry_count", 0)
                        exec_record.logs = final_state.get("logs", [])
                        db.commit()
                except Exception as db_err:
                    logger.warning(f"Failed to update workflow execution checkpoint: {db_err}")
                finally:
                    db.close()

    except Exception as e:
        logger.error(f"Error during LangGraph execution for {request_id}: {e}", exc_info=True)
        final_state["status"] = "failed"
        final_state["error_message"] = str(e)
        final_state["logs"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "orchestrator",
            "action": "workflow_failed",
            "message": f"Execution halted with unhandled error: {str(e)}",
            "status": "failed"
        })
        ACTIVE_WORKFLOWS[request_id] = final_state

    # Final DB Persistence
    db = SessionLocal()
    try:
        req = db.query(ContentRequest).filter(ContentRequest.id == request_id).first()
        exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.request_id == request_id).first()

        content_record = None
        current_content = final_state.get("current_content")

        if current_content:
            md_text = content_to_markdown(current_content)
            word_count = len(md_text.split())
            status_str = "approved" if final_state.get("is_published") else ("manual_review" if final_state.get("status") == "manual_review" else "draft")

            content_record = GeneratedContent(
                request_id=request_id,
                version=final_state.get("retry_count", 0) + 1,
                title=current_content.get("title", topic),
                raw_json=current_content,
                markdown_text=md_text,
                word_count=word_count,
                is_published=final_state.get("is_published", False),
                status=status_str
            )
            db.add(content_record)
            db.flush()

            final_state["content_id"] = content_record.id
            ACTIVE_WORKFLOWS[request_id] = final_state

        eval_data = final_state.get("latest_evaluation")
        if eval_data and content_record:
            eval_record = EvaluationReport(
                request_id=request_id,
                content_id=content_record.id,
                iteration=final_state.get("retry_count", 0) + 1,
                factual_accuracy=eval_data.get("factual_accuracy", 0.0),
                relevance=eval_data.get("relevance", 0.0),
                completeness=eval_data.get("completeness", 0.0),
                clarity_readability=eval_data.get("clarity_readability", 0.0),
                educational_effectiveness=eval_data.get("educational_effectiveness", 0.0),
                structure_organization=eval_data.get("structure_organization", 0.0),
                overall_score=eval_data.get("overall_score", 0.0),
                passed=eval_data.get("passed", False),
                identified_errors=eval_data.get("identified_errors", []),
                missing_concepts=eval_data.get("missing_concepts", []),
                improvement_recommendations=eval_data.get("improvement_recommendations", []),
                unsupported_claims=eval_data.get("unsupported_claims", [])
            )
            db.add(eval_record)

        revisions = final_state.get("revision_history", [])
        for rev in revisions:
            rev_record = RevisionHistory(
                request_id=request_id,
                iteration=rev.get("iteration", 1),
                changes_summary=rev.get("changes_summary", ""),
                previous_score=rev.get("previous_score", 0.0),
                new_score=eval_data.get("overall_score", 0.0) if eval_data else 0.0,
                modified_sections=rev.get("modified_sections", [])
            )
            db.add(rev_record)

        final_status = "completed" if final_state.get("is_published") else ("manual_review" if final_state.get("status") == "manual_review" else "failed")
        if req:
            req.status = final_status
        if exec_record:
            exec_record.status = final_status
            exec_record.completed_at = datetime.utcnow()
            exec_record.current_agent = final_state.get("current_agent", "supervisor")
            exec_record.logs = final_state.get("logs", [])
            exec_record.retry_count = final_state.get("retry_count", 0)
            if final_state.get("error_message"):
                exec_record.error_message = final_state.get("error_message")

        db.commit()
        logger.info(f"Workflow execution persisted successfully for request_id: {request_id}")
    except Exception as e:
        logger.error(f"Error finalizing DB persistence for {request_id}: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import GeneratedContent, EvaluationReport, ContentRequest
from app.schemas import AnalyticsResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Computes system-wide educational quality analytics, pass rates, and dimension metrics.
    """
    total_generated = db.query(GeneratedContent).count()
    approved_count = db.query(GeneratedContent).filter(GeneratedContent.status == "approved").count()
    manual_review_count = db.query(GeneratedContent).filter(GeneratedContent.status == "manual_review").count()
    failed_count = db.query(GeneratedContent).filter(GeneratedContent.status == "failed").count()

    eval_count = db.query(EvaluationReport).count()
    avg_score = db.query(func.avg(EvaluationReport.overall_score)).scalar() or 0.0

    pass_rate = round((approved_count / total_generated * 100), 1) if total_generated > 0 else 0.0

    # Dimension averages
    dim_accuracy = db.query(func.avg(EvaluationReport.factual_accuracy)).scalar() or 0.0
    dim_relevance = db.query(func.avg(EvaluationReport.relevance)).scalar() or 0.0
    dim_completeness = db.query(func.avg(EvaluationReport.completeness)).scalar() or 0.0
    dim_clarity = db.query(func.avg(EvaluationReport.clarity_readability)).scalar() or 0.0
    dim_educational = db.query(func.avg(EvaluationReport.educational_effectiveness)).scalar() or 0.0
    dim_structure = db.query(func.avg(EvaluationReport.structure_organization)).scalar() or 0.0

    dimension_averages = {
        "Factual Accuracy (25%)": round(dim_accuracy, 1),
        "Relevance (20%)": round(dim_relevance, 1),
        "Completeness (20%)": round(dim_completeness, 1),
        "Clarity & Readability (15%)": round(dim_clarity, 1),
        "Educational Effectiveness (10%)": round(dim_educational, 1),
        "Structure & Organization (10%)": round(dim_structure, 1)
    }

    # Score Distribution buckets
    all_scores = [r[0] for r in db.query(EvaluationReport.overall_score).all()]
    distribution = {
        "<60": sum(1 for s in all_scores if s < 60),
        "60-69": sum(1 for s in all_scores if 60 <= s < 70),
        "70-79": sum(1 for s in all_scores if 70 <= s < 80),
        "80-89": sum(1 for s in all_scores if 80 <= s < 90),
        "90-100": sum(1 for s in all_scores if 90 <= s <= 100),
    }

    # Recent activity
    recent_items = (
        db.query(GeneratedContent)
        .order_by(GeneratedContent.created_at.desc())
        .limit(6)
        .all()
    )

    recent_activity = []
    for item in recent_items:
        latest_eval = (
            db.query(EvaluationReport)
            .filter(EvaluationReport.content_id == item.id)
            .order_by(EvaluationReport.iteration.desc())
            .first()
        )
        recent_activity.append({
            "id": item.id,
            "title": item.title,
            "status": item.status,
            "score": latest_eval.overall_score if latest_eval else 0.0,
            "is_published": item.is_published,
            "created_at": item.created_at.isoformat()
        })

    return AnalyticsResponse(
        total_generated=total_generated,
        approved_count=approved_count,
        manual_review_count=manual_review_count,
        failed_count=failed_count,
        average_quality_score=round(avg_score, 1),
        pass_rate_percentage=pass_rate,
        dimension_averages=dimension_averages,
        score_distribution=distribution,
        recent_activity=recent_activity
    )


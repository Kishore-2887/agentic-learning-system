import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, SessionLocal
from app.api import content_router, workflow_router, analytics_router, settings_router
from app.utils.seed_data import seed_initial_demo_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("agentic-learning-system")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB tables and initial sample data
    logger.info("Initializing SQLite database tables...")
    init_db()
    db = SessionLocal()
    try:
        seed_initial_demo_data(db)
    except Exception as e:
        logger.error(f"Error seeding demo data: {e}")
    finally:
        db.close()
    logger.info("Backend service initialized successfully.")
    yield
    logger.info("Backend service shutting down.")


app = FastAPI(
    title="Agentic AI Learning Content Generation & Self-Evaluation System",
    description="Multi-agent orchestration platform using LangGraph for autonomous curriculum drafting, dimensional quality scoring, iterative remediation, and verified publication.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local dev frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(content_router)
app.include_router(workflow_router)
app.include_router(analytics_router)
app.include_router(settings_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Agentic AI Learning Content Generation & Evaluation",
        "active_provider": settings.LLM_PROVIDER,
        "default_quality_threshold": settings.DEFAULT_QUALITY_THRESHOLD,
        "max_retries": settings.MAX_IMPROVEMENT_ATTEMPTS
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)


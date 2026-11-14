from app.api.routes_content import router as content_router
from app.api.routes_workflow import router as workflow_router
from app.api.routes_analytics import router as analytics_router
from app.api.routes_settings import router as settings_router

__all__ = ["content_router", "workflow_router", "analytics_router", "settings_router"]


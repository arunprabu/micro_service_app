from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.api.deps import DbSession
from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Liveness + database check")
def health(db: DbSession, response: Response) -> dict[str, str]:
    settings = get_settings()
    try:
        db.execute(text("SELECT 1"))
        database = "up"
    except Exception:
        database = "down"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": "ok" if database == "up" else "degraded",
        "service": settings.app_name,
        "version": settings.app_version,
        "database": database,
    }

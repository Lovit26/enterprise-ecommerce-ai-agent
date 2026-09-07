from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.api.routes.orders import router as orders_router
from backend.core.config import settings
from backend.db.dependencies import get_db

from backend.api.routes.chat import router as chat_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(orders_router)
app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/health/db")
def database_health_check(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
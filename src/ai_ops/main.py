
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from ai_ops.api.ai import router as ai_router

from ai_ops.api.analytics import router as analytics_router
from ai_ops.db.session import check_database_connection

app = FastAPI(
    title="AI Operations Copilot",
    description=(
        "An AI-powered assistant for business analytics "
        "and operational knowledge."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)
app.include_router(ai_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Operations Copilot",
    }


@app.get("/health/db")
def database_health_check():
    try:
        check_database_connection()
        return {
            "status": "healthy",
            "database": "connected",
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "unavailable",
            },
        )

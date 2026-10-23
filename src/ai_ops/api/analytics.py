
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError

from ai_ops.analytics import (
    get_monthly_revenue,
    get_revenue_by_category,
    get_top_customers,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/revenue-by-category")
def revenue_by_category():
    try:
        data = get_revenue_by_category()
        return data.to_dict(orient="records")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve category revenue.",
        )


@router.get("/monthly-revenue")
def monthly_revenue():
    try:
        data = get_monthly_revenue()
        return data.to_dict(orient="records")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve monthly revenue.",
        )


@router.get("/top-customers")
def top_customers(limit: int = Query(default=10, ge=1, le=100)):
    try:
        data = get_top_customers(limit=limit)
        return data.to_dict(orient="records")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve top customers.",
        )

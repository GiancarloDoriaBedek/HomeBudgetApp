from fastapi import APIRouter, Depends, Query, status
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.auth_service import get_current_user
from app.services.spending_aggregation_service import get_total_spending

spending_aggregation_router = APIRouter(
    prefix="/aggregate",
    tags=["Report"]
)

@spending_aggregation_router.get(
    "/",
    summary="Get total spending",
    description=(
        "Calculate the total spending of the authenticated user, "
        "optionally filtered by date range and category."
    ),
    status_code=status.HTTP_200_OK)
def total_spending(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    total = get_total_spending(db, current_user.id, start_date, end_date, category_id)

    return {"total_spending": total}

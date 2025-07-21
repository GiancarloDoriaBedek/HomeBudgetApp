from fastapi import APIRouter, Depends, Query
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

@spending_aggregation_router.get("/")
def total_spending(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    total = get_total_spending(db, current_user.id, start_date, end_date, category_id)

    return {"total_spending": total}

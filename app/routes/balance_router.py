from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.expense import Expense
from app.models.user import User
from app.services.auth_service import get_current_user


balance_router = APIRouter(
    prefix="/balance",
    tags=["Balance"]
)

@balance_router.get("/balance", summary="Get current balance")
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_spent = db.query(Expense).filter(Expense.user_id == current_user.id).with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    current_balance = float(current_user.starting_balance) - float(total_spent or 0)
    return {
        "starting_balance": float(current_user.starting_balance), 
        "total_spent": float(total_spent), 
        "current_balance": current_balance
        }

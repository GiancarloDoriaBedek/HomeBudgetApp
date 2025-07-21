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

@balance_router.get(
        "/", 
        summary="Get current balance",
        description=(
        "Returns the user's current financial balance.\n\n"
        "- `starting_balance`: The users initial balance.\n"
        "- `total_spent`: Total expenses recorded by the user.\n"
        "- `current_balance`: The remaining balance (starting balance minus total spent)."),
    operation_id="get_current_balance")
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

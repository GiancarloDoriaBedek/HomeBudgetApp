from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseCreate, ExpenseUpdate
from app.models.user import User

def create_expense(db: Session, expense_data: ExpenseCreate, user: User) -> Expense:
    expense = Expense(**expense_data.dict(), user_id=user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses(
    db: Session,
    user: User,
    category_id: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Expense]:
    query = db.query(Expense).filter(Expense.user_id == user.id)

    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if min_amount:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount:
        query = query.filter(Expense.amount <= max_amount)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.all()


def get_expense(db: Session, expense_id: int, user: User) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user.id).first()

def update_expense(db: Session, expense_id: int, update_data: ExpenseUpdate, user: User) -> Expense | None:
    expense = get_expense(db, expense_id, user)
    if not expense:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int, user: User) -> bool:
    expense = get_expense(db, expense_id, user)
    if not expense:
        return False
    db.delete(expense)
    db.commit()
    return True

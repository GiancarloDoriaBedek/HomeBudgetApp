from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.schemas.expense_schema import ExpenseCreate, ExpenseUpdate, ExpenseRead
from app.models.user import User
from app.db import get_db
from app.services.auth_service import get_current_user
from app.services.expense_service import (
    create_expense,
    get_expenses,
    get_expense,
    update_expense,
    delete_expense
)

expense_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@expense_router.post(
    "/",
    response_model=ExpenseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Create a new expense record for the authenticated user.")
def create_new_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_expense(db, expense, current_user)


@expense_router.get(
    "/",
    response_model=List[ExpenseRead],
    summary="Get expenses with optional filters",
    description=(
        "Retrieve a list of expenses for the authenticated user, "
        "optionally filtered by category, amount range, and date range."))
def read_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    category_id: Optional[int] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    return get_expenses(
        db, current_user,
        category_id=category_id,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date
    )

@expense_router.get(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Get expense by ID",
    description="Retrieve a single expense by its ID if owned by the authenticated user.",
    responses={404: {"description": "Expense not found"}})
def read_single_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = get_expense(db, expense_id, current_user)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return expense


@expense_router.put(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Update an existing expense",
    description="Update expense details if it belongs to the authenticated user.",
    responses={404: {"description": "Expense not found or not owned by user"}})
def update_existing_expense(
    expense_id: int,
    update_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = update_expense(db, expense_id, update_data, current_user)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or not yours")
    
    return expense


@expense_router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Delete an expense by ID if it belongs to the authenticated user.",
    responses={404: {"description": "Expense not found or not owned by user"}})
def delete_existing_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_expense(db, expense_id, current_user)
    if not success:

        raise HTTPException(status_code=404, detail="Expense not found or not yours")
    


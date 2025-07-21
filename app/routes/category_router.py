from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryRead
from app.models.user import User
from app.db import get_db
from app.services.auth_service import get_current_user
from app.services.category_service import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category
)


category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_category(db, category, current_user)


@category_router.get("/", response_model=List[CategoryRead])
def read_user_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_categories(db, current_user)


@category_router.get("/{category_id}", response_model=CategoryRead)
def read_single_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = get_category(db, category_id, current_user)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.put("/{category_id}", response_model=CategoryRead)
def update_existing_category(
    category_id: int,
    update_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = update_category(db, category_id, update_data, current_user)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or not yours")
    return category


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_category(db, category_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or not yours")

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserSchema
from app.services.auth_service import get_current_active_user
from app.services.user_service import create_user, delete_user, get_user, get_users


user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@user_router.get('/', response_model=List[UserSchema], summary="List all users")
def user_list(db: Session = Depends(get_db)):
    db_users = get_users(db)

    return db_users


@user_router.get('/me', response_model=UserSchema, summary="Get current authenticated user")
def user_list(current_user: User = Depends(get_current_active_user)):
    return current_user



@user_router.get('/{user_id}', response_model=UserSchema, summary="Get user details by ID")
def user_detail(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user by ID")
def user_delete(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user(db, db_user.id)
    return {"message": "User deleted"}


@user_router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def user_post(user: UserCreate, db:Session = Depends(get_db)):
    return create_user(db, user)
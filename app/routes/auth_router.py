from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import Annotated
from app.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import authenticate_user, create_access_token
from app.db import get_db

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@auth_router.post(
    '/token',
    response_model=Token,
    summary="User login and token generation",
    description=(
        "Authenticate user credentials and generate a JWT access token.\n\n"
        "The token expires after 1440 minutes (1 day).\n\n"
        "Use this endpoint to obtain a Bearer token for authenticated requests."
    ),
    status_code=status.HTTP_200_OK,
    operation_id="login_for_access_token"
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
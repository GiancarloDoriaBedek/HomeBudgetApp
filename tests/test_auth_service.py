import pytest
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    JWT_SECRET_KEY,
    ALGORITHM,
)
from app.models.user import User
from app.models.token import TokenData
import jwt
import asyncio

class DummyUser:
    def __init__(self, email, password):
        self.email = email
        self.password = password


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.mark.asyncio
async def test_authenticate_user_success(mocker, mock_db):
    """
    Test successful authentication
    """
    user = DummyUser(email="user@test.com", password="hashedpassword")
    mocker.patch("app.services.auth_service.get_user_by_email", return_value=user)
    mocker.patch("app.services.auth_service.verify_password", return_value=True)

    result = authenticate_user("user@test.com", "plaintextpassword", mock_db)
    assert result == user


@pytest.mark.asyncio
async def test_authenticate_user_fail_wrong_password(mocker, mock_db):
    """
    Test authentication failure when password is incorrect
    """
    user = DummyUser(email="user@test.com", password="hashedpassword")
    mocker.patch("app.services.auth_service.get_user_by_email", return_value=user)
    mocker.patch("app.services.auth_service.verify_password", return_value=False)

    result = authenticate_user("user@test.com", "wrongpassword", mock_db)
    assert result is False


@pytest.mark.asyncio
async def test_authenticate_user_fail_no_user(mocker, mock_db):
    """
    Test authentication failure when user does not exist
    """
    mocker.patch("app.services.auth_service.get_user_by_email", return_value=None)

    result = authenticate_user("nouser@test.com", "password", mock_db)
    assert result is False


def test_create_access_token_contains_exp_and_sub():
    """
    Test that the access token contains exp and sub claims
    """
    data = {"sub": "user@test.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=10))

    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload
    assert payload["sub"] == "user@test.com"


@pytest.mark.asyncio
async def test_get_current_user_success(mocker):
    """
    Test retrieval of current user from token
    """
    user = DummyUser(email="user@test.com", password="hashedpassword")
    token_data = {"sub": user.email, "exp": datetime.now(timezone.utc).timestamp() + 600}

    test_token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)

    mocker.patch("app.services.auth_service.get_user_by_email", return_value=user)

    result = await get_current_user(test_token, db=None)
    assert result == user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mocker):
    """
    Test failure when the token is invalid, expect HTTP 401
    """
    invalid_token = "invalid.token.value"

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(invalid_token, db=None)
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_user_not_found(mocker):
    """
    Test failure when the user from token not fount, expecting HTTP 401
    """
    token_data = {"sub": "user@test.com", "exp": datetime.now(timezone.utc).timestamp() + 600}
    test_token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)

    mocker.patch("app.services.auth_service.get_user_by_email", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(test_token, db=None)
    assert exc_info.value.status_code == 401
    

@pytest.mark.asyncio
async def test_get_current_active_user_returns_user():
    """
    Test that get_current_active_user returns the user passed to it
    """
    user = DummyUser(email="user@test.com", password="hashedpassword")
    result = await get_current_active_user(user)
    assert result == user

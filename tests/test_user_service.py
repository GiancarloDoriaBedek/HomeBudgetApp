import pytest
from unittest.mock import MagicMock
from app.services.user_service import (
    get_users,
    get_user,
    get_user_by_email,
    create_user,
    delete_user,
)
from app.models.user import User
from app.schemas.user_schema import UserCreate

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()

def test_get_users_returns_list(mock_db):
    """
    Test get_users returns a list of User objects
    """
    mock_db.query.return_value.all.return_value = [User(id=1), User(id=2)]
    users = get_users(mock_db)

    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users)


def test_get_user_returns_user_when_found(mock_db):
    """
    Test get_user returns a User object when a user with given id exists
    """
    expected_user = User(id=1)
    mock_db.query.return_value.filter.return_value.first.return_value = expected_user
    user = get_user(mock_db, 1)

    assert user == expected_user


def test_get_user_returns_none_when_not_found(mock_db):
    """
    Test get_user returns None when user with given id does not
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None
    user = get_user(mock_db, 999)

    assert user is None


def test_get_user_by_email_returns_user(mock_db):
    """
    Test get_user_by_email returns a user whem email exists
    """
    expected_user = User(email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = expected_user
    user = get_user_by_email(mock_db, "test@example.com")
    assert user == expected_user


def test_create_user_adds_and_commits_user(mock_db, mocker):
    """
    Test create_user hashes password, adds user to db
    """
    user_create = UserCreate(email="test@example.com", username="testuser", password="secret")
    hashed_password = "hashed_secret"
    mocker.patch("app.services.user_service.get_password_hash", return_value=hashed_password)

    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    user = create_user(mock_db, user_create)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert user.email == user_create.email
    assert user.username == user_create.username
    assert user.password == hashed_password


def test_delete_user_deletes_and_commits_when_found(mock_db):
    """
    Test delete_user deletes
    """
    user = User(id=1)
    mock_db.query.return_value.filter.return_value.first.return_value = user
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    delete_user(mock_db, 1)

    mock_db.delete.assert_called_once_with(user)
    mock_db.commit.assert_called_once()

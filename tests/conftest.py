import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense

@pytest.fixture(scope="function")
def engine():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

@pytest.fixture(scope="function")
def db(engine):
    # Create all tables
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db):
    user = User(email="test@example.com", username="testuser", password="hashed_password")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def another_user(db):
    user = User(email="other@example.com", username="otheruser", password="hashed_password")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

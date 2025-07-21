import pytest
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services.category_service import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
)

def test_create_category(db: Session, test_user):
    category_data = CategoryCreate(name="Test Category")
    category = create_category(db, category_data, test_user)
    
    assert isinstance(category, Category)
    assert category.name == "Test Category"
    assert category.user_id == test_user.id


def test_get_categories_returns_all_user_categories(db: Session, test_user):
    create_category(db, CategoryCreate(name="Cat1"), test_user)
    create_category(db, CategoryCreate(name="Cat2"), test_user)

    categories = get_categories(db, test_user)

    assert len(categories) >= 2
    assert all(cat.user_id == test_user.id for cat in categories)


def test_get_category_returns_correct_category(db: Session, test_user):
    category = create_category(db, CategoryCreate(name="UniqueCat"), test_user)
    fetched = get_category(db, category.id, test_user)

    assert fetched is not None
    assert fetched.id == category.id
    assert fetched.user_id == test_user.id


def test_get_category_returns_none_for_wrong_user(db: Session, test_user, another_user):
    category = create_category(db, CategoryCreate(name="OtherUserCat"), another_user)
    result = get_category(db, category.id, test_user)

    assert result is None


def test_update_category_success(db: Session, test_user):
    category = create_category(db, CategoryCreate(name="OldName"), test_user)
    update_data = CategoryUpdate(name="NewName")

    updated_category = update_category(db, category.id, update_data, test_user)

    assert updated_category is not None
    assert updated_category.name == "NewName"
    

def test_delete_category_success(db: Session, test_user):
    category = create_category(db, CategoryCreate(name="DeleteMe"), test_user)
    result = delete_category(db, category.id, test_user)

    assert result is True
    assert get_category(db, category.id, test_user) is None

from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.models.user import User

def create_category(db: Session, category_data: CategoryCreate, user: User) -> Category:
    category = Category(**category_data.dict(), user_id=user.id)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session, user: User) -> list[Category]:
    return db.query(Category).filter(Category.user_id == user.id).all()


def get_category(db: Session, category_id: int, user: User) -> Category | None:
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()


def update_category(db: Session, category_id: int, update_data: CategoryUpdate, user: User) -> Category | None:
    category = get_category(db, category_id, user)
    if not category:
        return None
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int, user: User) -> bool:
    category = get_category(db, category_id, user)
    if not category:
        return False
    
    db.delete(category)
    db.commit()

    return True

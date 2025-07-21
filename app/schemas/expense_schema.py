from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExpenseBase(BaseModel):
    description: Optional[str] = None
    amount: float = Field(..., gt=0)
    category_id: int
    date: Optional[datetime] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    date: Optional[datetime] = None


class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ExpenseRead(BaseModel):
    id: int
    description: Optional[str]
    amount: float
    date: datetime
    category: CategoryRead

    class Config:
        orm_mode = True

from fastapi import FastAPI
from app.routes import auth, category, expense
from app.db import Base, engine

app = FastAPI(
    title="Home Budget API",
    description="A simple REST API for tracking home expenses.",
    version="1.0.0"
)

# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(category.router, prefix="/categories", tags=["Categories"])
# app.include_router(expense.router, prefix="/expenses", tags=["Expenses"])

Base.metadata.create_all(bind=engine)
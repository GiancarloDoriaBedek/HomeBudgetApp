from fastapi import FastAPI
from app.routes import auth_router, user_router, category_router, expense_router, balance_router, spending_aggregation_router
from app.db import Base, engine

app = FastAPI(
    title="Home Budget API",
    description="A simple REST API for tracking home expenses.",
    version="1.0.0"
)

app.include_router(auth_router.auth_router, prefix="/api")
app.include_router(user_router.user_router,  prefix="/api", tags=["Users"])
app.include_router(category_router.category_router, prefix="/api", tags=["Categories"])
app.include_router(expense_router.expense_router, prefix="/api", tags=["Expenses"])
app.include_router(spending_aggregation_router.spending_aggregation_router, prefix="/api")
app.include_router(balance_router.balance_router, prefix="/api")

Base.metadata.create_all(bind=engine)
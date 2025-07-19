from sqlalchemy import text
from app.db import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.fetchone())
except Exception as e:
    print("Database connection failed:", e)

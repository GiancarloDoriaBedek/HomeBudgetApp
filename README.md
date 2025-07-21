# Home Budget App

A personal finance management API built with FastAPI to track expenses

## Features

- User registration and authentication (JWT-based).
- Expense management: create, read, update, delete.
- Category management: create, read, update, delete.
- Aggregate spending reports filtered by date range and category.
- Secure access to user data.
- API documentation with Swagger UI.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL (or other SQL databases)
- Pydantic for data validation
- OAuth2 with JWT for authentication
- Alembic for database migrations
- pytest for testing
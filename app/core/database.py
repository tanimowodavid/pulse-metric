"""Database configuration and session management for Pulse Metric.

This module exposes:
- `engine`: the SQLAlchemy engine configured from `DATABASE_URL`.
- `SessionLocal`: a session factory for request-scoped database sessions.
- `get_db`: FastAPI dependency that yields a database session and closes it after use.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://user:password@localhost:5432/pulse_metric",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a database session for the duration of a single request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

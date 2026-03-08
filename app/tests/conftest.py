"""Pytest fixtures for API and database integration tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db


# Test database URL (separate from the main development database).
TEST_DATABASE_URL = "postgresql+psycopg://user:password@db:5432/pulse_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create all tables once per test session and drop them afterwards."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide an isolated database session per test with rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Return a TestClient wired to use the test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override the real DB dependency with the test DB in the app logic.
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base

# We define a TEST database URL. 
# We'll use a different database name so we don't accidentally delete your dev data.
TEST_DATABASE_URL = "postgresql+psycopg://user:password@db:5432/pulse_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Builds the database tables once before we run any tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provides a fresh database session for a single test and rolls back changes after."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Provides a 'Secret Shopper' client that uses the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    # This 'overrides' the real DB with our test DB in the app logic
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
    
"""Integration test configuration and fixtures."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.db_models import Base

# Use a real file-based SQLite database for integration testing
# This ensures we test actual file persistence, not just in-memory behavior
TEST_DB_FILE = "test_integration.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{TEST_DB_FILE}"

# Create engine with check_same_thread=False for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for the test session."""
    # Ensure clean slate
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Patch the application's engine/SessionLocal to use our test engine
    # This is necessary because LegacyDatabaseWrapper uses SessionLocal directly
    import app.database
    app.database.engine = engine
    app.database.SessionLocal = TestingSessionLocal
    
    yield engine
    
    # Cleanup after all tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)



@pytest.fixture
def db_session(db_engine):
    """Create a fresh database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

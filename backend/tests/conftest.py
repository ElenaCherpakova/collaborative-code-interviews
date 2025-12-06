"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import db


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test."""
    db._interviews.clear()
    yield
    db._interviews.clear()

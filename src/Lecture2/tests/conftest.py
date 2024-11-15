from typing import Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.models.user_model import User
from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.db.session import get_db as real_get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

"""
This override allows your endpoints that 
depend on get_current_user to receive a test user, 
test_db_session, test_whatever, etc,
without actual authentication, harrassing.
"""

# Override the get_db dependency
def override_get_db() -> Generator[Session, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Mock the current user for authentication
def override_get_current_user() -> User:
    """Pretend we are mocking Keycloak for authentication"""
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        is_active=True,
        is_superuser=False
    )
    return user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
async def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client

"""Pytest configuration and fixtures."""

import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.config import settings


# Test database URL (in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
    }


@pytest.fixture
def test_organization_data():
    """Sample organization data for tests."""
    return {
        "name": "Test Organization",
        "slug": "test-org",
        "description": "A test organization",
        "industry": "Technology",
    }


@pytest.fixture
def sample_trait_data():
    """Sample trait data for tests."""
    return {
        "name": "Test Trait",
        "category": "COGNITIVE",
        "definition": "A test trait definition",
        "spectrum_low_label": "Low",
        "spectrum_high_label": "High",
        "behavioral_markers_low": ["marker1", "marker2"],
        "behavioral_markers_high": ["marker3", "marker4"],
        "counter_indicator_for": ["Role1"],
        "display_order": 1,
    }

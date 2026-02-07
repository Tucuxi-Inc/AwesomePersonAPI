"""
Tests for database initialization and seeding (init_db.py).

Tests the individual functions using mocked database sessions since
the models use PostgreSQL-specific types (UUID, JSONB) not available in SQLite.
"""

import pytest
import uuid
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone

from app.core.security import verify_password
from app.db.init_db import (
    create_superuser,
    create_test_user,
    create_demo_organization,
)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _mock_db_session(existing_record=None):
    """Create a mock database session that returns the given record for queries."""
    db = MagicMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = existing_record
    db.execute.return_value = result
    return db


# ── create_superuser ──────────────────────────────────────────────────────────


class TestCreateSuperuser:
    """Tests for create_superuser function."""

    def test_creates_new_superuser(self):
        db = _mock_db_session(existing_record=None)
        user = create_superuser(db)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()
        added_user = db.add.call_args[0][0]
        assert added_user.email == "admin@apapi.dev"
        assert added_user.role == "ADMIN"
        assert added_user.is_superuser is True
        assert added_user.is_active is True
        assert verify_password("changeme123", added_user.hashed_password)

    def test_returns_existing_superuser(self):
        existing = MagicMock()
        existing.email = "admin@apapi.dev"
        db = _mock_db_session(existing_record=existing)
        result = create_superuser(db)
        assert result is existing
        db.add.assert_not_called()


# ── create_test_user ──────────────────────────────────────────────────────────


class TestCreateTestUser:
    """Tests for create_test_user function."""

    def test_creates_new_test_user(self):
        org_id = uuid.uuid4()
        db = _mock_db_session(existing_record=None)
        user = create_test_user(db, org_id)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        added_user = db.add.call_args[0][0]
        assert added_user.email == "test@example.com"
        assert added_user.role == "INTERVIEWER"
        assert added_user.is_superuser is False
        assert added_user.organization_id == org_id
        assert verify_password("changeme123", added_user.hashed_password)

    def test_returns_existing_test_user(self):
        existing = MagicMock()
        existing.email = "test@example.com"
        db = _mock_db_session(existing_record=existing)
        result = create_test_user(db, uuid.uuid4())
        assert result is existing
        db.add.assert_not_called()


# ── create_demo_organization ──────────────────────────────────────────────────


class TestCreateDemoOrganization:
    """Tests for create_demo_organization function."""

    def test_creates_new_organization(self):
        db = _mock_db_session(existing_record=None)
        org = create_demo_organization(db)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        added_org = db.add.call_args[0][0]
        assert added_org.name == "Demo Organization"
        assert added_org.slug == "demo"
        assert added_org.industry == "Technology"
        assert added_org.is_active is True

    def test_returns_existing_organization(self):
        existing = MagicMock()
        existing.name = "Demo Organization"
        existing.slug = "demo"
        db = _mock_db_session(existing_record=existing)
        result = create_demo_organization(db)
        assert result is existing
        db.add.assert_not_called()

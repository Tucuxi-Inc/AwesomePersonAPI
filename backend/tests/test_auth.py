"""Tests for authentication functionality."""

import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)


class TestPasswordHashing:
    """Test password hashing functions."""

    def test_password_hash_is_different_from_plain(self):
        """Hashed password should be different from plain password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password

    def test_verify_correct_password(self):
        """Correct password should verify successfully."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Incorrect password should fail verification."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_different_passwords_have_different_hashes(self):
        """Different passwords should have different hashes."""
        hash1 = get_password_hash("password1")
        hash2 = get_password_hash("password2")
        assert hash1 != hash2


class TestTokens:
    """Test JWT token functions."""

    def test_create_access_token(self):
        """Access token should be created successfully."""
        token = create_access_token(subject="test-user-id")
        assert token is not None
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Refresh token should be created successfully."""
        token = create_refresh_token(subject="test-user-id")
        assert token is not None
        assert len(token) > 0

    def test_verify_valid_access_token(self):
        """Valid access token should verify successfully."""
        user_id = "test-user-id"
        token = create_access_token(subject=user_id)
        verified_id = verify_token(token, token_type="access")
        assert verified_id == user_id

    def test_verify_valid_refresh_token(self):
        """Valid refresh token should verify successfully."""
        user_id = "test-user-id"
        token = create_refresh_token(subject=user_id)
        verified_id = verify_token(token, token_type="refresh")
        assert verified_id == user_id

    def test_access_token_fails_with_refresh_type(self):
        """Access token should fail when verified as refresh type."""
        token = create_access_token(subject="test-user-id")
        result = verify_token(token, token_type="refresh")
        assert result is None

    def test_refresh_token_fails_with_access_type(self):
        """Refresh token should fail when verified as access type."""
        token = create_refresh_token(subject="test-user-id")
        result = verify_token(token, token_type="access")
        assert result is None

    def test_invalid_token_fails_verification(self):
        """Invalid token should fail verification."""
        result = verify_token("invalid-token", token_type="access")
        assert result is None

"""Encryption utilities for sensitive data storage.

Uses Fernet symmetric encryption to protect sensitive values like SMTP passwords
stored in the database.
"""

import base64
import hashlib
import logging
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from app.config import settings

logger = logging.getLogger(__name__)


def get_fernet_key() -> bytes:
    """
    Derive a Fernet-compatible key from SECRET_KEY.

    Fernet requires a 32-byte base64-encoded key. We derive this from
    the application's SECRET_KEY using SHA-256.

    Returns:
        bytes: A 32-byte base64-encoded key suitable for Fernet.
    """
    key_bytes = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def encrypt_value(plaintext: str) -> str:
    """
    Encrypt a string value using Fernet symmetric encryption.

    Args:
        plaintext: The string value to encrypt.

    Returns:
        The encrypted value as a base64-encoded string.
    """
    fernet = Fernet(get_fernet_key())
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt_value(ciphertext: str) -> Optional[str]:
    """
    Decrypt a Fernet-encrypted string.

    Args:
        ciphertext: The encrypted value as a base64-encoded string.

    Returns:
        The decrypted plaintext string, or None if decryption fails.
    """
    try:
        fernet = Fernet(get_fernet_key())
        return fernet.decrypt(ciphertext.encode()).decode()
    except InvalidToken:
        logger.error("Failed to decrypt value: invalid token or key mismatch")
        return None
    except Exception as e:
        logger.error("Failed to decrypt value: %s", str(e))
        return None

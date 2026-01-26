"""Custom exceptions for the application."""

from typing import Any, Optional


class APAPIException(Exception):
    """Base exception for AP API."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(APAPIException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed", details: Optional[dict[str, Any]] = None):
        super().__init__(message, code="AUTHENTICATION_ERROR", details=details)


class AuthorizationError(APAPIException):
    """User not authorized for this action."""

    def __init__(self, message: str = "Not authorized", details: Optional[dict[str, Any]] = None):
        super().__init__(message, code="AUTHORIZATION_ERROR", details=details)


class NotFoundError(APAPIException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: Any = None):
        details = {"resource": resource}
        if identifier:
            details["identifier"] = str(identifier)
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            details=details,
        )


class ValidationError(APAPIException):
    """Validation failed."""

    def __init__(self, message: str, field: Optional[str] = None, details: Optional[dict[str, Any]] = None):
        details = details or {}
        if field:
            details["field"] = field
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class ConflictError(APAPIException):
    """Resource conflict (e.g., duplicate)."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, code="CONFLICT", details=details)

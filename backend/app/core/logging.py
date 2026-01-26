"""Logging configuration."""

import logging
import sys
from typing import Any

from app.config import settings


def setup_logging() -> None:
    """Configure logging for the application."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.DEBUG else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)


class AuditLogger:
    """Logger for audit trail entries."""

    def __init__(self):
        self.logger = get_logger("audit")

    def log(
        self,
        action: str,
        user_id: str | None,
        resource_type: str,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Log an audit event."""
        self.logger.info(
            f"AUDIT: action={action} user={user_id} "
            f"resource={resource_type}:{resource_id} details={details}"
        )


audit_logger = AuditLogger()

import logging
import sys

from app.config import settings


def setup_logging() -> logging.Logger:
    """Configure structured logging for the application."""

    # Create logger
    logger = logging.getLogger("ias12")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Format: timestamp - level - message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()

"""
=========================================================
AI Data Analyzer Pro
Logging Utility
=========================================================
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.settings import settings

# ==========================================================
# LOGGER CONFIGURATION
# ==========================================================

_LOGGER_CACHE = {}


def _create_formatter() -> logging.Formatter:
    """
    Create standard log formatter.
    """

    return logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _create_console_handler() -> logging.Handler:
    """
    Create console handler.
    """

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(_create_formatter())

    return console_handler


def _create_file_handler() -> logging.Handler:
    """
    Create rotating file handler.
    """

    log_path = Path(settings.logging.LOG_FILE)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setFormatter(_create_formatter())

    return file_handler


# ==========================================================
# PUBLIC LOGGER
# ==========================================================

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return configured logger.

    Example
    -------
    logger = get_logger(__name__)
    """

    logger_name = name or "AI_Data_Analyzer"

    if logger_name in _LOGGER_CACHE:

        return _LOGGER_CACHE[logger_name]

    logger = logging.getLogger(logger_name)

    logger.setLevel(getattr(logging, settings.logging.LOG_LEVEL.upper(), logging.INFO))

    logger.propagate = False

    if not logger.handlers:

        logger.addHandler(_create_console_handler())

        logger.addHandler(_create_file_handler())

    _LOGGER_CACHE[logger_name] = logger

    return logger


# ==========================================================
# DEFAULT LOGGER
# ==========================================================

logger = get_logger("AI_Data_Analyzer")


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [
    "get_logger",
    "logger",
]

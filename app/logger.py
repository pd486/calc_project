"""Centralized logging setup."""

import logging
import os

from app.calculator_config import CalculatorConfig

_configured = False


def configure_logging(config: CalculatorConfig) -> logging.Logger:
    """Configure the calculator logger."""

    global _configured

    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)

    if _configured:
        return logger

    os.makedirs(config.log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(
        config.log_file,
        encoding=config.default_encoding,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False

    _configured = True
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the calculator logger."""
    return logging.getLogger(f"calculator.{name}")
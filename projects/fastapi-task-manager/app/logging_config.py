"""Application logging setup."""

import logging
from pathlib import Path


def configure_logging() -> logging.Logger:
    """Configure console and file logging without exposing sensitive data."""
    project_root = Path(__file__).resolve().parents[1]
    log_path = project_root / "logs" / "app.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("task_manager")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = configure_logging()

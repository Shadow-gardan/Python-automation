"""Application logging configuration."""

import logging
from pathlib import Path


def configure_logging(log_path: Path, level: int = logging.INFO) -> logging.Logger:
	"""Configure console and file logging and return the application logger."""
	log_path.parent.mkdir(parents=True, exist_ok=True)
	logger = logging.getLogger("automation")
	logger.setLevel(level)
	logger.propagate = False

	if logger.handlers:
		return logger

	formatter = logging.Formatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)
	file_handler = logging.FileHandler(log_path, encoding="utf-8")
	file_handler.setFormatter(formatter)
	console_handler = logging.StreamHandler()
	console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	return logger
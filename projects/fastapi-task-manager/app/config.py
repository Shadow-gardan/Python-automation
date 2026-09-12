"""Environment-aware application settings."""

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = f"sqlite:///{PROJECT_ROOT / 'data' / 'tasks.db'}"


@dataclass(frozen=True)
class Settings:
    """Runtime settings with safe local defaults."""

    app_name: str = os.getenv("APP_NAME", "FastAPI Task Management REST API")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    testing: bool = os.getenv("TESTING", "false").lower() == "true"


settings = Settings()

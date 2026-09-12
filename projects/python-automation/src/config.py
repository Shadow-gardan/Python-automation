"""Project paths and application settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "automation.db"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_PATH = LOG_DIR / "app.log"
CUSTOMER_INPUT_PATH = INPUT_DIR / "customers.csv"
CLEANED_CUSTOMER_PATH = OUTPUT_DIR / "cleaned_customers.csv"
REPORT_PATH = OUTPUT_DIR / "report.txt"
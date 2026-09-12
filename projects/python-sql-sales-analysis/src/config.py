"""Project paths and settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "sales_analysis.db"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_PATH = LOG_DIR / "app.log"
SALES_INPUT_PATH = INPUT_DIR / "sales.csv"
CLEANED_SALES_PATH = OUTPUT_DIR / "cleaned_sales.csv"

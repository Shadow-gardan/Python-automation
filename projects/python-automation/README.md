# Python File & Data Automation Tool

A production-minded, beginner-readable Python automation application for organizing files, cleaning customer CSV data, storing records in SQLite, and generating a useful summary report.

## Features

- Categorizes and copies files into Images, Documents, Spreadsheets, Videos, Audio, Archives, and Other folders.
- Preserves original input files and avoids overwriting duplicate output names.
- Cleans CSV data by normalizing headers, replacing missing values with `N/A`, and removing duplicate rows.
- Stores cleaned customer data in SQLite with parameterized SQL queries.
- Reports customer counts, average age, city distribution, and missing information.
- Writes structured application logs to `logs/app.log`.
- Provides a concise `argparse` command-line interface.
- Includes pytest coverage for file organization, CSV processing, and database queries.

## Technologies

Python 3, SQLite, SQL, pytest, Git/GitHub, and Linux/Ubuntu. Runtime functionality uses Python's standard library; pytest is the only development dependency.

## Architecture

```text
Input files
	↓
Python automation and file organization
	↓
CSV cleaning and duplicate removal
	↓
SQLite storage
	↓
SQL analysis
	↓
Text summary report
```

The workflow is intentionally split into small modules so each stage can be
tested or reused independently.

## Project Structure

```text
python-automation/
├── data/input/              # Original sample files and customers.csv
├── data/output/             # Cleaned CSV, organized copies, and reports
├── database/                # Local SQLite database (ignored by Git)
├── logs/                    # Runtime logs (ignored by Git)
├── src/
│   ├── config.py            # Relative project paths
│   ├── database.py          # SQLite schema, import, and queries
│   ├── data_processor.py    # CSV/JSON loading and CSV cleaning
│   ├── file_organizer.py    # Safe copy-based file organization
│   ├── logger.py            # Logging setup
│   ├── main.py              # CLI and workflow orchestration
│   └── report_generator.py  # JSON and text reports
└── tests/                   # Automated tests
```

## Installation

```bash
git clone https://github.com/Shadow-gardan/Python-automation.git
cd Python-automation/projects/python-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run commands from the `python-automation` directory:

```bash
python -m src.main organize
python -m src.main clean-csv
python -m src.main import-db
python -m src.main report
python -m src.main run-all
```

`run-all` organizes the input files, cleans `customers.csv`, imports the cleaned records into SQLite, runs SQL analysis, and writes `data/output/report.txt`. If that report already exists, a timestamped report is created instead of overwriting it.

## Testing

```bash
pytest -v
```

Tests use temporary directories and in-memory databases, so they do not modify project data.

## Example

The sample `data/input/customers.csv` contains eight rows, including one
duplicate customer record and three missing values. Running `run-all` creates a
cleaned CSV with seven rows, stores those rows in SQLite, and writes a report
under `data/output/` with customer counts, average age, and city statistics.

## Safety

The file organizer copies files by default. It never deletes originals and never overwrites an existing output file. Local databases, logs, virtual environments, cache files, and environment files are excluded from Git.

## Future Improvements

- Excel support
- PostgreSQL support
- Web dashboard
- Scheduled automation
- REST API
- Docker support

## Portfolio Value

This project demonstrates practical freelance skills: filesystem automation, data cleaning, duplicate detection, missing-value handling, SQLite and SQL reporting, structured logging, exception handling, CLI design, testing, and Git-based delivery.

## Freelance Use Case

The same pattern can automate repetitive file organization, clean incoming
client CSV exports, import data into a database, run repeatable SQL reports,
and deliver a readable summary without modifying original source files.

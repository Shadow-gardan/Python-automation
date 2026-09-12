# Python File & Data Automation Tool

The first version organizes files by extension, processes CSV/JSON records, and
writes a small JSON report. It is the foundation for a larger automation project
that will later add SQL storage and logging.

## Structure

```text
python-automation/
├── data/input/              # Files and data to process
├── data/output/             # Generated categories and reports
├── logs/                    # Runtime logs
├── src/
│   ├── main.py
│   ├── file_organizer.py
│   ├── data_processor.py
│   └── report_generator.py
└── tests/test_file_organizer.py
```

## Run

Create and activate a virtual environment, then run the tests and organizer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m unittest discover -s tests -v
PYTHONPATH=src python src/main.py
```

The organizer copies files from `data/input` into folders such as `Images`,
`Documents`, and `Other` under `data/output`. Existing files are preserved by
adding a numeric suffix to duplicate names. The CSV/JSON processor normalizes
field names and the report generator writes a record-count summary.

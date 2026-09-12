# Python Developer | Automation | SQL | FastAPI

I build practical Python tools for repetitive workflows, data processing, database reporting, and backend APIs.

This repository contains three portfolio projects that demonstrate file and data automation, CSV and JSON processing, SQL database operations, data cleaning, business reporting, REST API development, and testable application design. The projects are designed to be readable, reproducible, and useful as starting points for small business workflows.

## Projects

### 1. Python File & Data Automation Tool

[Open the project](projects/python-automation/)

An end-to-end command-line workflow for:

- Organizing files into categories while preserving originals and avoiding overwrites.
- Loading and cleaning CSV and JSON data.
- Removing duplicate rows and filling missing CSV values.
- Importing cleaned customer data into SQLite with parameterized SQL.
- Generating customer summaries and text reports.
- Logging application stages and testing the workflow with pytest.

The project includes 10 passing tests and uses Python's standard library at runtime.

### 2. Python + SQL Sales & Customer Data Analysis System

[Open the project](projects/python-sql-sales-analysis/)

A repeatable sales-data workflow for:

- Validating CSV structure, dates, quantities, prices, and customer/product fields.
- Cleaning text and dates, removing exact duplicates, and rejecting invalid rows.
- Loading sales data into normalized SQLite tables for customers, products, orders, and order items.
- Running SQL analytics for revenue, orders, products, customers, cities, categories, months, and average spending.
- Generating timestamped business reports without overwriting existing reports.
- Logging processing stages and covering the workflow with pytest.

The project includes 13 passing tests and uses transactions, foreign keys, and parameterized SQL values.

### 3. FastAPI Task Management REST API

[Open the project](projects/fastapi-task-manager/)

A documented backend API for managing tasks with:

- FastAPI REST endpoints for task creation, reading, updating, and deletion.
- SQLite persistence through SQLAlchemy.
- Pydantic validation for task fields, statuses, priorities, dates, and query parameters.
- Status and priority filtering with skip/limit pagination.
- Clear 404 and 422 error responses.
- Structured logging and isolated pytest coverage.
- Swagger UI and OpenAPI documentation through `/docs` and `/openapi.json`, plus ReDoc through `/redoc`.

The project includes 14 passing tests and HTTPX-backed API testing through FastAPI's test client.

## Services I Can Provide

### Python Automation

- Automate repetitive file and folder processing.
- Process CSV and JSON files.
- Generate repeatable text reports.
- Build small Python utilities and Linux automation workflows.

### Python + SQL

- Write SQL queries and database operations.
- Load CSV data into SQLite databases.
- Clean, validate, and deduplicate incoming data.
- Produce database-backed reports and analysis scripts.

### FastAPI Backend Development

- Develop REST APIs and CRUD endpoints.
- Integrate SQLite with SQLAlchemy.
- Add request validation with Pydantic.
- Implement filtering, pagination, API tests, and Swagger/OpenAPI documentation.

## Technology Stack

Python, SQL, SQLite, SQLAlchemy, FastAPI, Pydantic, pytest, HTTPX, Git, GitHub, Linux/Ubuntu, CSV, and JSON.

## Project Quality

The projects demonstrate:

- Automated tests: 37 tests pass across the three projects.
- Input validation and explicit error handling.
- Logging of useful workflow and application events.
- Safe database operations using SQLite, transactions where appropriate, foreign keys, and parameterized SQL.
- Reproducible virtual-environment setup and command-line workflows.
- Git version control and project-level documentation.

The tests use temporary directories or isolated databases where appropriate, so routine test runs do not depend on production data.

## Development Environment

The projects are developed and tested on Linux/Ubuntu. Each project contains its own README with installation, usage, testing, and configuration details. Local virtual environments, databases, logs, caches, and environment files are excluded from Git by the project ignore rules.

## Contact and Hiring

I am available for small Python automation tasks, data-processing scripts, SQL/database work, and FastAPI backend projects.

GitHub: [Shadow-gardan](https://github.com/Shadow-gardan)

## Repository Notes

This is a practical project portfolio. It documents capabilities demonstrated by the code and tests in this repository and does not claim client work, commercial results, or certifications.

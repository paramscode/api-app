# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python FastAPI data backend application that provides REST endpoints for generating test data files in CSV format. The main functionality includes a CSV generation endpoint that creates files based on user-specified parameters.

## Development Setup

The project uses a Python 3.12 virtual environment located at `venv/`. Dependencies are managed via `requirements.txt`.

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
# OR
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/test_main.py -v

# Run tests with coverage
pytest tests/test_main.py -v --cov=src --cov-report=html --cov-report=term
```

## Application Architecture

- **src/main.py**: FastAPI application with two endpoints:
  - `POST /generate-csv`: Generates CSV files with test data
  - `GET /health`: Health check endpoint
- **src/**: Source code directory with subdirectories for api, models, and services
- **tests/test_main.py**: Unit tests using pytest and FastAPI's TestClient
- **requirements.txt**: Dependencies including FastAPI, uvicorn, pydantic, pytest, pytest-cov, and httpx

## API Endpoints

- `POST /generate-csv`: Accepts `{"numberOfEnrollments": int}` and returns a CSV file with that many rows of test data
- `GET /health`: Returns `{"status": "healthy"}`

## Testing

The project uses pytest with FastAPI's TestClient. Tests cover:
- Health check functionality
- CSV generation with various input sizes
- Request validation
- Response format verification

## Development Commands

- Start server: `python -m src.main` or `uvicorn src.main:app --reload`
- Run tests: `pytest tests/test_main.py -v`
- Run tests with coverage: `pytest tests/test_main.py -v --cov=src --cov-report=html --cov-report=term`
- API docs: http://localhost:8000/docs (when server is running)

## Notes

- The application generates CSV files in memory using Python's csv module
- CSV responses include proper headers for file download
- The .gitignore includes patterns for Abstra and various Python development tools
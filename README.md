# Data Backend API

This is a Python FastAPI application that provides REST endpoints for generating test data files in CSV format.

## Features

- **CSV Generation Endpoint**: POST `/generate-csv` - Creates a CSV file with test data based on the number of enrollments requested
- **Health Check**: GET `/health` - Simple health check endpoint

## Local Development Setup

### Prerequisites
- Python 3.12

### Setup Steps

1. **Create and activate virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m src.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API will be available at: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Usage

### Generate CSV
```bash
curl -X POST "http://localhost:8000/generate-csv" \
     -H "Content-Type: application/json" \
     -d '{"numberOfEnrollments": 5}' \
     --output enrollments.csv
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Running Tests

```bash
# Run tests
pytest tests/test_main.py -v

# Run tests with coverage report
pytest tests/test_main.py -v --cov=src --cov-report=html --cov-report=term
```

## Project Structure

```
data-backend/
├── src/                 # Source code directory
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── api/             # API endpoints (future)
│   ├── models/          # Data models (future)
│   └── services/        # Business logic (future)
├── tests/               # Test directory
│   ├── __init__.py
│   └── test_main.py     # Unit tests
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── CLAUDE.md           # Claude Code guidance
└── venv/               # Virtual environment
```
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

## Docker Deployment

### Prerequisites
- Docker installed on your system

### Build and Run with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t api-app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 api-app
   ```

3. **Run with file logging enabled:**
   ```bash
   docker run -p 8000:8000 -e ENABLE_FILE_LOGGING=true api-app
   ```

4. **Run in detached mode:**
   ```bash
   docker run -d -p 8000:8000 --name api-app-container api-app
   ```

5. **Access the API:**
   - API will be available at: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs

### Docker Management Commands

```bash
# Stop the container
docker stop api-app-container

# Start the container
docker start api-app-container

# View logs
docker logs api-app-container

# Remove container
docker rm api-app-container

# Remove image
docker rmi api-app
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
api-app/
├── src/                 # Source code directory
│   ├── main.py          # FastAPI application entry point
│   ├── api/             # API layer
│   │   └── endpoints/   # API endpoint handlers
│   │       ├── csv.py   # CSV generation endpoint
│   │       └── health.py # Health check endpoint
│   ├── config/          # Configuration modules
│   │   └── logging.py   # Logging configuration
│   ├── middleware/      # FastAPI middleware
│   │   └── logging.py   # Request logging middleware
│   ├── models/          # Pydantic data models
│   └── services/        # Business logic services
├── tests/               # Test directory
├── requirements.txt     # Python dependencies
```
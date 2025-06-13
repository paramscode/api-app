# CLAUDE.md
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

# Run tests
pytest tests/test_main.py -v

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

### Running the Application
- Start server: `python -m src.main` or `uvicorn src.main:app --reload`
- Start server with file logging: `ENABLE_FILE_LOGGING=true python -m src.main`
- API docs: http://localhost:8000/docs (when server is running)

### Testing and Validation Commands
**IMPORTANT**: Always activate the virtual environment before running tests or validation commands:

```bash
# Activate virtual environment (required for all commands below)
source venv/bin/activate

# Run unit tests
pytest tests/test_main.py -v

# Run tests with coverage report
pytest tests/test_main.py -v --cov=src --cov-report=html --cov-report=term

# Run tests with coverage and fail if coverage is below threshold
pytest tests/test_main.py -v --cov=src --cov-fail-under=80

# Install new dependencies after updating requirements.txt
pip install -r requirements.txt
```

### Validation Workflow
When making changes, ALWAYS follow this validation sequence:

1. **Activate virtual environment**: `source venv/bin/activate`
2. **Install dependencies** (if requirements.txt changed): `pip install -r requirements.txt`
3. **Run tests**: `pytest tests/test_main.py -v`
4. **Check coverage**: `pytest tests/test_main.py -v --cov=src --cov-report=term`
5. **Start application** (optional): `python -m src.main`
6. **Test endpoints** (optional): Visit http://localhost:8000/docs

### TDD Development Workflow
For new features or bug fixes, follow this Test-Driven Development approach:

1. **Understand requirements**: Clearly define what the feature/fix should do
2. **Write failing tests**: Create test cases that describe expected behavior
   ```bash
   source venv/bin/activate
   pytest tests/test_main.py::test_new_feature -v  # Should fail initially
   ```
3. **Implement minimal code**: Write just enough code to make tests pass
4. **Validate tests pass**: Run tests to confirm implementation works
   ```bash
   pytest tests/test_main.py -v
   ```
5. **Refactor and optimize**: Improve code quality while keeping tests green
6. **Final validation**: Run full test suite with coverage
   ```bash
   pytest tests/test_main.py -v --cov=src --cov-report=term
   ```

## Coding Standards and Best Practices

### Logging Standards
- **Use structured JSON logging**: All logging should use the centralized logging configuration in `src/config/logging.py`
- **Include request IDs**: Every log entry should include the request ID for traceability using `get_request_id()`
- **Log at appropriate levels**: 
  - INFO: Normal operations, successful requests
  - WARNING: Unusual conditions that may need attention
  - ERROR: Errors that prevent normal operation
  - DEBUG: Detailed diagnostic information (development only)
- **Performance logging**: Log processing times for operations that may be slow
- **Structured extra data**: Use the `extra` parameter to include structured data in logs

### Code Organization
- **Follow directory structure**: Keep code organized in the established `src/` structure
- **Separation of concerns**: 
  - `src/api/endpoints/`: HTTP endpoint handlers
  - `src/models/`: Pydantic models for request/response validation
  - `src/services/`: Business logic and external service interactions
  - `src/config/`: Configuration modules
  - `src/middleware/`: FastAPI middleware components
- **Use dependency injection**: Leverage FastAPI's dependency injection system for shared resources

### Error Handling
- **Use FastAPI exceptions**: Always use `HTTPException` for API errors with appropriate status codes
- **Consistent error responses**: Return structured error responses with meaningful messages
- **Log errors with context**: Include relevant context (request data, user info, etc.) in error logs
- **Handle edge cases**: Validate inputs and handle boundary conditions gracefully

### Documentation
- **Document all endpoints**: Use FastAPI's automatic documentation features
- **Type hints**: Use comprehensive type hints for all functions and methods
- **Docstrings**: Include docstrings for all public functions, classes, and modules
- **API documentation**: Ensure OpenAPI docs are accurate and complete

### Testing and Test-Driven Development (TDD)
- **Follow TDD workflow**: Write tests first, then implement code to make tests pass
  1. **Red**: Write a failing test that describes the desired functionality
  2. **Green**: Write the minimal code needed to make the test pass
  3. **Refactor**: Improve code quality while keeping tests passing
- **Test first approach**: Before adding new features or fixing bugs:
  1. Write test cases that define expected behavior
  2. Run tests to confirm they fail (Red)
  3. Implement the feature/fix to make tests pass (Green)
  4. Refactor and optimize code while maintaining test success (Refactor)
- **Maintain high test coverage**: Aim for 80%+ test coverage using pytest
- **Test categories to include**:
  - **Unit tests**: Test individual functions and methods in isolation
  - **Integration tests**: Test API endpoints using FastAPI's TestClient
  - **Error case tests**: Test error conditions and edge cases
  - **Validation tests**: Test input validation and boundary conditions
- **Use test fixtures**: Leverage pytest fixtures for common test setup and teardown
- **Test naming convention**: Use descriptive test names that explain what is being tested
- **Arrange-Act-Assert pattern**: Structure tests clearly with setup, execution, and verification phases

### Security
- **Input validation**: Use Pydantic models for strict input validation
- **Sanitize outputs**: Ensure outputs don't expose sensitive information
- **No secrets in code**: Never commit secrets, use environment variables
- **Rate limiting**: Implement rate limiting for resource-intensive endpoints
- **Request size limits**: Set appropriate limits on request sizes

### Performance
- **Use async/await**: Use asynchronous programming patterns throughout
- **Implement pagination**: For endpoints that return large datasets
- **Monitor response times**: Log and monitor API response times
- **Resource management**: Properly close files, connections, and other resources
- **Optimize database queries**: Use efficient query patterns and indexing

### Code Quality
- **Consistent formatting**: Use consistent code formatting (consider using black/isort)
- **Meaningful names**: Use descriptive variable and function names
- **Keep functions small**: Break down complex functions into smaller, focused functions
- **Avoid code duplication**: Extract common functionality into reusable functions
- **Handle exceptions gracefully**: Don't let exceptions bubble up without proper handling

## Environment Variables

### Logging Configuration
- **ENABLE_FILE_LOGGING**: Set to `true` to enable file logging (default: disabled)
  - When disabled: Logs only to console
  - When enabled: Logs to both console and rotating log files (`app.log`)
  
Examples:
```bash
# Console logging only (default)
python -m src.main

# Enable file logging
ENABLE_FILE_LOGGING=true python -m src.main

# Run tests with file logging enabled
ENABLE_FILE_LOGGING=true pytest tests/test_main.py -v
```

## Notes

- The application generates CSV files in memory using Python's csv module
- CSV responses include proper headers for file download
- The .gitignore includes patterns for various Python development tools
- **Logging configuration**:
  - **Default**: Console logging only for cleaner development
  - **File logging**: Enable with `ENABLE_FILE_LOGGING=true` for production
  - **Rotating logs**: When enabled, creates rotating log files with 10MB max size, 5 backups
- Request IDs are automatically generated and included in all log entries for request tracing
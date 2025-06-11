import csv
import io
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_generate_csv_valid_request():
    """Test CSV generation with a valid request."""
    response = client.post("/generate-csv", json={"numberOfEnrollments": 3})
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment; filename=enrollments.csv" in response.headers["content-disposition"]
    
    # Parse CSV content
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    # Check header
    assert rows[0] == ["enrollment_id", "data"]
    
    # Check data rows
    assert len(rows) == 4  # header + 3 data rows
    assert rows[1] == ["1", "hello"]
    assert rows[2] == ["2", "hello"]
    assert rows[3] == ["3", "hello"]


def test_generate_csv_zero_enrollments():
    """Test CSV generation with zero enrollments."""
    response = client.post("/generate-csv", json={"numberOfEnrollments": 0})
    
    assert response.status_code == 200
    
    # Parse CSV content
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    # Should only have header
    assert len(rows) == 1
    assert rows[0] == ["enrollment_id", "data"]


def test_generate_csv_large_number():
    """Test CSV generation with a larger number of enrollments."""
    response = client.post("/generate-csv", json={"numberOfEnrollments": 100})
    
    assert response.status_code == 200
    
    # Parse CSV content
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    # Check we have the right number of rows
    assert len(rows) == 101  # header + 100 data rows
    assert rows[0] == ["enrollment_id", "data"]
    assert rows[1] == ["1", "hello"]
    assert rows[100] == ["100", "hello"]


def test_generate_csv_invalid_request():
    """Test CSV generation with invalid request body."""
    response = client.post("/generate-csv", json={"invalidField": 5})
    
    assert response.status_code == 422  # Validation error
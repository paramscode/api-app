import csv
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.models import EnrollmentRequest

router = APIRouter()


@router.post("/generate-csv")
async def generate_csv(request: EnrollmentRequest):
    """Generate a CSV file with test data based on the number of enrollments."""
    
    # Create CSV content in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["enrollment_id", "data"])
    
    # Write data rows
    for i in range(request.numberOfEnrollments):
        writer.writerow([i + 1, "hello"])
    
    # Get CSV content
    csv_content = output.getvalue()
    output.close()
    
    # Create streaming response
    csv_io = io.StringIO(csv_content)
    
    return StreamingResponse(
        io.BytesIO(csv_content.encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=enrollments.csv"}
    )
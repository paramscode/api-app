import csv
import io
import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.models import EnrollmentRequest
from src.config.logging import get_logger, get_request_id

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate-csv")
async def generate_csv(request: EnrollmentRequest):
    """Generate a CSV file with test data based on the number of enrollments."""
    
    start_time = time.time()
    request_id = get_request_id()
    
    logger.info(
        "CSV generation started",
        extra={
            "number_of_enrollments": request.numberOfEnrollments,
            "request_id": request_id
        }
    )
    
    # Validate input
    if request.numberOfEnrollments < 0:
        logger.warning(
            "Invalid enrollment count requested",
            extra={
                "number_of_enrollments": request.numberOfEnrollments,
                "request_id": request_id
            }
        )
        raise HTTPException(status_code=400, detail="Number of enrollments must be greater than or equal to 0")
    
    if request.numberOfEnrollments > 100000:
        logger.warning(
            "Large enrollment count requested",
            extra={
                "number_of_enrollments": request.numberOfEnrollments,
                "request_id": request_id
            }
        )
    
    try:
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
        
        # Calculate metrics
        file_size = len(csv_content.encode('utf-8'))
        process_time = time.time() - start_time
        
        logger.info(
            "CSV generation completed successfully",
            extra={
                "number_of_enrollments": request.numberOfEnrollments,
                "file_size_bytes": file_size,
                "process_time_seconds": round(process_time, 4),
                "request_id": request_id
            }
        )
        
        # Create streaming response
        return StreamingResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=enrollments.csv"}
        )
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "CSV generation failed",
            extra={
                "number_of_enrollments": request.numberOfEnrollments,
                "error": str(e),
                "error_type": type(e).__name__,
                "process_time_seconds": round(process_time, 4),
                "request_id": request_id
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to generate CSV file")
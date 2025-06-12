from fastapi import APIRouter
from src.config.logging import get_logger, get_request_id

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    request_id = get_request_id()
    
    logger.info(
        "Health check performed",
        extra={
            "status": "healthy",
            "request_id": request_id
        }
    )
    
    return {"status": "healthy"}
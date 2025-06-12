import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.config.logging import get_logger, set_request_id, get_request_id

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses with structured logging."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate and set request ID
        request_id = set_request_id()
        
        # Log request
        start_time = time.time()
        logger.info(
            "HTTP request started",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_host": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
                "content_length": request.headers.get("content-length"),
                "request_id": request_id
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log successful response
            logger.info(
                "HTTP request completed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time_seconds": round(process_time, 4),
                    "response_size": response.headers.get("content-length"),
                    "request_id": request_id
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Calculate processing time for failed requests
            process_time = time.time() - start_time
            
            # Log error
            logger.error(
                "HTTP request failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "process_time_seconds": round(process_time, 4),
                    "request_id": request_id
                },
                exc_info=True
            )
            
            # Re-raise the exception
            raise
from fastapi import FastAPI
from src.api.endpoints import csv, health
from src.config.logging import setup_logging, get_logger
from src.middleware.logging import LoggingMiddleware

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="Data Backend API", version="1.0.0")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

app.include_router(csv.router)
app.include_router(health.router)

logger.info("Application started", extra={"app_name": "Data Backend API", "version": "1.0.0"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import logging
import logging.config
import os
import sys
import uuid
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger

request_id_var: ContextVar[str] = ContextVar('request_id', default='')


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get('')
        return True


def setup_logging(level: str = "INFO"):
    """Configure structured JSON logging for the application.
    
    File logging is disabled by default. To enable file logging,
    set the environment variable: ENABLE_FILE_LOGGING=true
    """
    
    # Check if file logging should be enabled
    enable_file_logging = os.getenv("ENABLE_FILE_LOGGING", "false").lower() == "true"
    
    # Build handlers list based on configuration
    handlers = ["console"]
    if enable_file_logging:
        handlers.append("file")
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": jsonlogger.JsonFormatter,
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s"
            },
            "console": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "filters": {
            "request_id": {
                "()": RequestIdFilter
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "console",
                "filters": ["request_id"]
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "json",
                "filters": ["request_id"]
            }
        },
        "loggers": {
            "": {  # root logger
                "level": level,
                "handlers": handlers,
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO", 
                "handlers": handlers,
                "propagate": False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


def set_request_id(request_id: str = None) -> str:
    """Set request ID for the current context."""
    if request_id is None:
        request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    return request_id


def get_request_id() -> str:
    """Get the current request ID."""
    return request_id_var.get('')
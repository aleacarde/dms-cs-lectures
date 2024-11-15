import os
from logging.config import dictConfig


LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

def setup_logging() -> None:
    """
    This function is called in the main app file (app/main.py)
    """
    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
            },
            "detailed": {
                "format": "[%(asctime)s] %(levelname)s - %(name)s - %(funcName)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "filename": "app.log",
                "level": LOG_LEVEL
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propogate": False
            }
        },
        "root": {
            "handlers": ["console"],
            "level": LOG_LEVEL
        }
    }

    dictConfig(logging_config)
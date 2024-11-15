# Creation of the FastAPI instance
# Inclusion of routers from different endpoints
# Middleware definitions
# Event handers (startup and shutdown)
import logging


from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.logging_middleware import SanitizationMiddleWare


# Initialize logging configuration
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

app.add_middleware(SanitizationMiddleWare)
app.include_router(api_router, prefix=settings.API_V1_PATH)

@app.get("/")
def read_root():
    app_logger = logging.getLogger("app")
    app_logger.info("Root endpoint was accessed")
    return {"message": "Welcome to the Calendar4 Backend!"}
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app")

class SanitizationMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method == "POST":
            body = await request.json()
            if "password" in body:
                body["password"] = "[REDACTED]"
            logger.info(f"Sanitized request body: {body}")
        
        response = await call_next(request)

        return response
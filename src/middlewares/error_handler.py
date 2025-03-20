from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

def setup_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, str) else "Unknown error"
        logger.warning(f"HTTP error {exc.status_code}: {detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": detail})
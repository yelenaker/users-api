from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception:
            return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

def setup_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, str) else "Unknown error"
        return JSONResponse(status_code=exc.status_code, content={"error": detail})

from typing import Annotated
from fastapi import FastAPI, Depends
from src.api import users
from src.middlewares import error_handler
import config
from functools import lru_cache
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@lru_cache
def get_settings():
    return config.Settings()

# Створення екземпляра FastAPI з необхідними метаданими
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
    }
]

app = FastAPI(
    title="Users API",
    description="API for user management",
    version="0.0.0",
    contact={
        "name": "Olena Mykhailovska",
        "email": "yelenaker@gmail.com",
    },
    openapi_tags=tags_metadata
)

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }

# Підключення маршрутизаторів і middleware
app.include_router(users.router)
app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)
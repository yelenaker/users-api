from typing import Annotated
from fastapi import FastAPI, Depends
from src.api import users
from src.middlewares import error_handler
import config
from functools import lru_cache
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@lru_cache
def get_settings():
    """Функция для получения кэшированных настроек."""
    return config.get_settings()

# Получаем настройки
settings = get_settings()

# Логируем, если приложение работает в тестовом режиме
if settings.TEST_MODE:
    logger.info("Приложение запущено в ТЕСТОВОМ режиме!")

# Метаданные API
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
    }
]

# Создание экземпляра FastAPI
app = FastAPI(
    title="Users API",
    description="API for user management",
    version=settings.APPLICATION_VERSION,
    contact={
        "name": "Olena Mykhailovska",
        "email": "yelenaker@gmail.com",
    },
    openapi_tags=tags_metadata
)

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    """Возвращает информацию о версии приложения и режиме работы."""
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE,
        "env_mode": settings.ENV_MODE
    }

@app.get("/")
async def root(settings: Annotated[config.Settings, Depends(get_settings)]):
    """Корневой маршрут API"""
    return {
        "message": "Users API is running",
        "version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }

# Подключение маршрутизаторов и middleware
app.include_router(users.router)
app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)
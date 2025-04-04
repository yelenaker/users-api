from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from config import get_settings
from src.models.users import Base  # Імпорт базової моделі

# Отримуємо конфігурацію Alembic
config = context.config

# Налаштування логування
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Вказуємо метадані для автогенерації міграцій
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запускає міграції в офлайн-режимі."""
    url = get_settings().DATABASE_URL  # Використовуємо DATABASE_URL з налаштувань
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запускає міграції в онлайн-режимі."""
    connectable = engine_from_config(
        {'sqlalchemy.url': get_settings().DATABASE_URL},  # Використовуємо DATABASE_URL з налаштувань
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import os
import sys
from decouple import config, Config, RepositoryEnv

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
config = Config(RepositoryEnv(env_path))


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Імпортуємо Base та моделі
from backend.database import Base
from backend.models import User, PostSearch


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

# URL підключення до бази даних
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql+asyncpg://{config('DB_USERNAME')}:{config("DB_PASSWORD")}5@{config('DB_HOST')}:{config('DB_PORT')}/{config("DB_NAME")}")

def run_migrations_offline():
    """Режим офлайн: генерація SQL скриптів без підключення до БД."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Режим онлайн: застосування міграцій до БД."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
            url=DATABASE_URL
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    """Налаштування контексту міграцій."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True  # Для SQLite, якщо потрібна підтримка
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())

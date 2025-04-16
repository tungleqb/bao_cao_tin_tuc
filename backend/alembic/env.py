from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

from backend.app.models import user, loai_baocao, report  # Import models
from backend.app.database import Base
from backend.app.config import settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy.ext.asyncio import AsyncEngine
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        async with context.begin_transaction():
            await context.run_migrations()

    import asyncio
    asyncio.run(connectable.connect().then(do_run_migrations))

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
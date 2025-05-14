import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Thêm backend vào sys.path để import app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base
from app.config import settings
from app.models import user, report_type, period, report, audit_log

# Lấy cấu hình từ alembic.ini
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Chuyển asyncpg ➔ psycopg2 cho Alembic (sync engine)
database_url = settings.DATABASE_URL.replace("asyncpg", "psycopg2")

# Bỏ qua các bảng hệ thống EDB, PostgreSQL
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and (
        name.startswith('edb$') or
        name.startswith('pg_') or
        name.startswith('dual') or
        name.startswith('callback_queue') or
        name.startswith('plsql')
    ):
        return False
    return True

def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

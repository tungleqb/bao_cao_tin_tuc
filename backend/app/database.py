# backend/app/database.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .config import settings

# Lấy DATABASE_URL từ biến môi trường hoặc .env
DATABASE_URL = settings.DATABASE_URL

# Tạo engine async
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Tạo session maker
async_session_maker = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Tạo Base để kế thừa trong models
Base = declarative_base()

# Hàm async dependency lấy session
@asynccontextmanager
async def get_async_session():
    async with async_session_maker() as session:
        yield session

# Tuỳ chọn: khởi tạo bảng nếu cần
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


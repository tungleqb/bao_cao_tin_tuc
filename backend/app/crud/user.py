# backend/app/crud/user.py (phiên bản chuẩn hóa)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..services.auth import get_password_hash
from datetime import datetime

async def create_user(db: AsyncSession, user_in: UserCreate):
    try:
        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = get_password_hash(user_in.password)
        user = User(
            username=user_in.username,
            hashed_password=hashed_password,
            name=user_in.name,
            time_created=datetime.now(),  # ✅ Thêm dòng này
            level=user_in.level,
            is_admin=user_in.is_admin,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:  
        print(f"❌ Error creating user: {e}")
        await db.rollback() # Rollback the transaction in case of error 
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_users(db: AsyncSession):
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"❌ Error fetching user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
    try:
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        stmt = update(User).where(User.id == user_id).values(**update_data)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error updating user with ID {user_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_user(db: AsyncSession, user_id: int):
    try:
        stmt = delete(User).where(User.id == user_id)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error deleting user with ID {user_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_password_only(db: AsyncSession, user_id: int, new_password: str):
    try:  
        hashed = get_password_hash(new_password)
        stmt = update(User).where(User.id == user_id).values(hashed_password=hashed)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error updating password for user with ID {user_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

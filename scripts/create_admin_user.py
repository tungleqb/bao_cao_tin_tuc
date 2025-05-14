# backend/scripts/create_admin_user.py

import asyncio
from datetime import datetime
from app.database import get_async_session
from app.services.auth import get_password_hash
from app.models.user import User

async def create_admin():
    async with get_async_session() as session:
        hashed_pw = get_password_hash("12345678")
        admin_user = User(
            username="admin",
            hashed_password=hashed_pw,
            name="Quản trị viên",
            time_created=datetime.now(),
            avatar=None,
            level="CAPPHONG",  # hoặc "ADMIN" nếu bạn định nghĩa riêng
            is_admin=True
        )
        session.add(admin_user)
        await session.commit()
        print("✅ Admin user created.")

if __name__ == "__main__":
    asyncio.run(create_admin())

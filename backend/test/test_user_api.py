import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from backend.app.main import app
from backend.app.services.auth import create_access_token
from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.services.auth import get_password_hash
from datetime import datetime

@pytest.mark.asyncio
async def test_crud_user():
    # Chuẩn bị database: đảm bảo có admin test
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.username == "testadmin1"))
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            new_admin = User(
                username="testadmin1",
                hashed_password=get_password_hash("adminpassword"),
                name="Test Admin",
                time_created=datetime.now(),
                level="CAPPHONG",
                is_admin=True,
            )
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)
            admin_user = new_admin

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # Tạo token từ user thực tế
        token = create_access_token({"sub": str(admin_user.id)})
        headers = {"Authorization": f"Bearer {token}"}

        # Tạo user mới
        create_payload = {
            "username": "testuser1",
            "password": "testpassword",
            "name": "Test User 1",
            "level": "CAPPHONG",
            "is_admin": False
        }
        resp = await ac.post("/admin/user/", json=create_payload, headers=headers)
        assert resp.status_code == 200, f"Create user failed: {resp.text}"
        user_data = resp.json()
        user_id = user_data["id"]

        # Lấy danh sách users
        resp = await ac.get("/admin/user/", headers=headers)
        assert resp.status_code == 200
        users = resp.json()
        assert any(u["username"] == "testuser1" for u in users)

        # Cập nhật user
        update_payload = {
            "name": "Test User 1 Updated",
            "level": "CAPXA",
            "is_admin": True
        }
        resp = await ac.put(f"/admin/user/{user_id}", json=update_payload, headers=headers)
        assert resp.status_code == 200

        # Xoá user
        resp = await ac.delete(f"/admin/user/{user_id}", headers=headers)
        assert resp.status_code == 200

        # Kiểm tra user đã bị xoá
        resp = await ac.get("/admin/user/", headers=headers)
        users = resp.json()
        assert not any(u["id"] == user_id for u in users)

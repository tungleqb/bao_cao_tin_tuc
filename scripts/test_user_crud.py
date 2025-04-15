import pytest
from httpx import AsyncClient
from ..backend.app.main import app

@pytest.mark.asyncio
async def test_crud_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Đăng nhập admin
        res = await client.post("/auth/login", data={
            "username": "admin",
            "password": "adminpassword"
        })
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Tạo user
        user_data = {
            "username": "testuser",
            "password": "123456",
            "ten_chi_nhanh": "CN test",
            "is_admin": False
        }
        res = await client.post("/admin/user", json=user_data, headers=headers)
        assert res.status_code == 200
        user_id = res.json()["id"]

        # Lấy danh sách
        res = await client.get("/admin/user", headers=headers)
        assert res.status_code == 200
        assert any(u["id"] == user_id for u in res.json())

        # Cập nhật
        user_data["username"] = "testuser_updated"
        res = await client.put(f"/admin/user/{user_id}", json=user_data, headers=headers)
        assert res.status_code == 200
        assert res.json()["username"] == "testuser_updated"

        # Xoá
        res = await client.delete(f"/admin/user/{user_id}", headers=headers)
        assert res.status_code == 200

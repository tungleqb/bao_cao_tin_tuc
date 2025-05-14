# backend/test/test_period.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://report_user:password@localhost:5444/baocao"

test_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
def anyio_backend():
    return 'asyncio'

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_crud_period(client: AsyncClient):
    payload = {
        "TYPE": "TEST",
        "ID": "TEST_001",
        "Name": "Kỳ báo cáo test",
        "ActiveAt": "2025-05-01T08:00:00",
        "DeactiveAt": "2025-05-10T17:00:00",
        "StartAt": "2025-05-01T09:00:00",
        "EndAt": "2025-05-10T15:00:00",
        "FromAt": "2025-05-01T00:00:00",
        "ToAt": "2025-05-10T00:00:00",

        "XaActiveAt": "2025-05-02T08:00:00",
        "XaDeactiveAt": "2025-05-11T17:00:00",
        "XaStartAt": "2025-05-02T09:00:00",
        "XaEndAt": "2025-05-11T15:00:00",
        "XaFromAt": "2025-05-02T00:00:00",
        "XaToAt": "2025-05-11T00:00:00",

        "Status": "Active",
        "XaStatus": "Deactive",
        "Killer": "Auto",
        "FolderPath": "/static/reports/TEST_001"
    }

    # Tạo mới
    resp = await client.post("/period/", json=payload)
    assert resp.status_code == 200

    # Lấy lại
    resp = await client.get(f"/period/{payload['ID']}")
    assert resp.status_code == 200
    assert resp.json()["Name"] == payload["Name"]

    # Cập nhật tên
    resp = await client.put(f"/period/{payload['ID']}", json={"Name": "Tên mới"})
    assert resp.status_code == 200
    assert resp.json()["Name"] == "Tên mới"

    # Xoá
    resp = await client.delete(f"/period/{payload['ID']}")
    assert resp.status_code == 200
    assert resp.json()["ok"] == True

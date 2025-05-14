# backend/test/test_report_api.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
import aiofiles

@pytest.mark.asyncio
async def test_upload_report_full_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        headers = {"Authorization": "Bearer fake-admin-token"}

        # Chuẩn bị file dummy
        dummy_file_content = b"dummy content for testing upload"
        dummy_filename = "dummy_test_file.txt"
        dummy_file_path = os.path.join("backend", "static", "reports", "BCNGAY_20250427", dummy_filename)
        
        # Tạo thư mục nếu cần
        os.makedirs(os.path.dirname(dummy_file_path), exist_ok=True)

        # Gửi yêu cầu upload
        files = {"file": (dummy_filename, dummy_file_content)}
        data = {
            "report_type_id": "BCNGAY",
            "period_id": "BCNGAY_20250427",
            "comment": "Test full report upload",
            "has_event": "true",
        }
        response = await ac.post("/report/upload", files=files, data=data, headers=headers)

        assert response.status_code in (200, 201)
        json_data = response.json()

        # Kiểm tra các field trong response
        assert "FileName" in json_data
        assert json_data["Comment"] == "Test full report upload"
        assert json_data["HasEvent"] is True
        assert isinstance(json_data["LateSeconds"], int)

        # Kiểm tra file đã lưu trên server
        assert os.path.exists(dummy_file_path)

@pytest.mark.asyncio
async def test_get_my_reports_after_upload():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        headers = {"Authorization": "Bearer fake-admin-token"}
        response = await ac.get("/report/user/reports", headers=headers)
        assert response.status_code == 200
        reports = response.json()
        assert isinstance(reports, list)
        assert len(reports) > 0

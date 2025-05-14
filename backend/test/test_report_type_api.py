import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app

@pytest.mark.asyncio
async def test_crud_report_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        headers = {"Authorization": "Bearer fake-admin-token"}

        # Xoá trước nếu ID đã tồn tại
        await ac.delete("/admin/loaibaocao/BCTEST", headers=headers)

        # Tạo mới
        payload = {
            "ID": "BCTEST",
            "DateCreated": "2025-04-27T00:00:00",
            "Name": "Báo cáo test",
            "Period_ID": "DAILY",  # Kiểm tra các giá trị hợp lệ của Period_ID
            "ActiveAt": "00:00:00",  # Giờ cho phép gửi báo cáo
            "DeactiveAt": "23:59:59",  # Giờ huỷ kích hoạt
            "StartAt": "08:00:00",  # Giờ bắt đầu
            "EndAt": "20:00:00",  # Giờ kết thúc
            "From": "00:00:00",  # Giờ lấy số liệu từ
            "To": "23:59:59",  # Giờ lấy số liệu đến
            "ActiveOffset": 0,  # Offset kích hoạt (số ngày lệch)
            "DeactiveOffset": 0,  # Offset huỷ kích hoạt (số ngày lệch)
            "StartOffset": 0,  # Offset bắt đầu (số ngày lệch)
            "EndOffset": 0,  # Offset kết thúc (số ngày lệch)
            "FromOffset": 0,  # Offset lấy số liệu từ (số ngày lệch)
            "ToOffset": 0,  # Offset lấy số liệu đến (số ngày lệch)
            "XaActiveOffset": 0,  # Offset kích hoạt cho CAPXA
            "XaDeactiveOffset": 0,  # Offset huỷ kích hoạt cho CAPXA
            "XaStartOffset": 0,  # Offset bắt đầu cho CAPXA
            "XaEndOffset": 0,  # Offset kết thúc cho CAPXA
            "XaFromOffset": 0,  # Offset lấy số liệu từ cho CAPXA
            "XaToOffset": 0,  # Offset lấy số liệu đến cho CAPXA
            "DocExtList": ".doc .docx .pdf .xls",  # Đuôi file hợp lệ
            "MaxSize": "100MB",  # Kích thước file tối đa
            "NextAt": None,  # Thời gian tiếp theo
        }
        resp = await ac.post("/admin/loaibaocao/", json=payload, headers=headers)
        assert resp.status_code in (200, 201)

        # Lấy danh sách
        resp = await ac.get("/admin/loaibaocao/", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert any(item["ID"] == "BCTEST" for item in data)

        # Cập nhật
        update_payload = {
            "Name": "Báo cáo test update",
            "Period_ID": "WEEKLY",  # Kiểm tra các giá trị hợp lệ của Period_ID
            "ActiveAt": "01:00:00",  # Giờ cho phép gửi báo cáo
            "DeactiveAt": "23:59:59",  # Giờ huỷ kích hoạt
            "StartAt": "08:00:00",  # Giờ bắt đầu
            "EndAt": "20:00:00",  # Giờ kết thúc
            "From": "00:00:00",  # Giờ lấy số liệu từ
            "To": "23:59:59",  # Giờ lấy số liệu đến
            "ActiveOffset": 1,  # Offset kích hoạt (số ngày lệch)
            "DeactiveOffset": 1,  # Offset huỷ kích hoạt (số ngày lệch)
            "StartOffset": 1,  # Offset bắt đầu (số ngày lệch)
            "EndOffset": 1,  # Offset kết thúc (số ngày lệch)
            "FromOffset": 1,  # Offset lấy số liệu từ (số ngày lệch)
            "ToOffset": 1,  # Offset lấy số liệu đến (số ngày lệch)
            "XaActiveOffset": 1,  # Offset kích hoạt cho CAPXA
            "XaDeactiveOffset": 1,  # Offset huỷ kích hoạt cho CAPXA
            "XaStartOffset": 1,  # Offset bắt đầu cho CAPXA
            "XaEndOffset": 1,  # Offset kết thúc cho CAPXA
            "XaFromOffset": 1,  # Offset lấy số liệu từ cho CAPXA
            "XaToOffset": 1,  # Offset lấy số liệu đến cho CAPXA
            "DocExtList": ".doc .docx .pdf .xls",  # Đuôi file hợp lệ
            "MaxSize": "100MB",  # Kích thước file tối đa
            "NextAt": "2025-05-01T00:00:00",  # Thời gian tiếp theo
        }
        resp = await ac.put("/admin/loaibaocao/BCTEST", json=update_payload, headers=headers)
        assert resp.status_code == 200

        # Xoá
        resp = await ac.delete("/admin/loaibaocao/BCTEST", headers=headers)
        assert resp.status_code == 200

# spec_loaibaocao.txt (cập nhật 28/04/2025)

# Đặc tả cấu trúc **LoaiBaoCao**

> Tài liệu nội bộ - dự án **Hệ thống báo cáo tin tức**

---

## 1. Mục đích

Mô tả chuẩn dữ liệu cho bảng **`LoaiBaoCao`**:

- Đồng bộ backend ↔ frontend;
- Hỗ trợ Scheduler tự động tạo/huỷ kỳ;
- Hỗ trợ quản lý 2 cấp chi nhánh: `CAPPHONG` và `CAPXA`;
- Tài liệu bảo trì mã nguồn sau này.

---

## 2. Các trường dữ liệu

| Trường | Kiểu | Bắt buộc | Mô tả | Mặc định |
|--------|------|----------|-------|------------------|
| ID | string | ✓ | Mã định danh | - |
| DateCreated | datetime | ✓ | Thời điểm tạo | now() |
| Name | string | ✓ | Tên loại báo cáo | - |
| Period_ID | enum | ✓ | Chu kỳ: DAILY, WEEKLY, MONTHLY, NONE | NONE |
| ActiveOn / DeactiveOn | int | ✓ | Ngày/thứ cho phép gửi - CAPPHONG | 0 |
| ActiveAt / DeactiveAt | time | ✓ | Giờ cho phép gửi - CAPPHONG | 00:00:00 / 23:59:59 |
| StartOn / EndOn | int | ✓ | Ngày/thứ đúng hạn - CAPPHONG | 0 |
| StartAt / EndAt | time | ✓ | Giờ đúng hạn - CAPPHONG | - |
| FromOn / ToOn | int | ✓ | Ngày/thứ lấy số liệu - CAPPHONG | 0 |
| From / To | time | ✓ | Giờ lấy số liệu - CAPPHONG | 00:00:00 / 23:59:59 |
| ActiveOffset / DeactiveOffset | int | × | Kỳ lệch - CAPPHONG | 0 |
| StartOffset / EndOffset | int | × | Kỳ lệch đúng hạn - CAPPHONG | 0 |
| FromOffset / ToOffset | int | × | Kỳ lệch lấy số liệu - CAPPHONG | 0 |
| XaActiveOn / XaDeactiveOn | int | × | Ngày/thứ cho phép gửi - CAPXA | 0 |
| XaActiveAt / XaDeactiveAt | time | × | Giờ cho phép gửi - CAPXA | 00:00:00 / 23:59:59 |
| XaStartOn / XaEndOn | int | × | Ngày/thứ đúng hạn - CAPXA | 0 |
| XaStartAt / XaEndAt | time | × | Giờ đúng hạn - CAPXA | - |
| XaFromOn / XaToOn | int | × | Ngày/thứ lấy số liệu - CAPXA | 0 |
| XaFrom / XaTo | time | × | Giờ lấy số liệu - CAPXA | 00:00:00 / 23:59:59 |
| XaActiveOffset / XaDeactiveOffset | int | × | Kỳ lệch - CAPXA | 0 |
| XaStartOffset / XaEndOffset | int | × | Kỳ lệch đúng hạn - CAPXA | 0 |
| XaFromOffset / XaToOffset | int | × | Kỳ lệch lấy số liệu - CAPXA | 0 |
| DocExtList | string | × | Đuôi file hợp lệ | .doc .docx .pdf .bm2 .jpg .xlsx .xls |
| MaxSize | string | × | Kích thước tối đa file | 100MB |
| NextAt | datetime | × | Lần scheduler tiếp theo | - |

---

## 3. Ghi chú

- **CAPPHONG** dùng nhóm trường gốc.
- **CAPXA** dùng nhóm trường `Xa*`.
- Các quy tắc Period_ID, ISO weekday, timezone server, ... giữ nguyên.

---

## 4. Công thức tính mốc thời gian

```python
anchor = get_anchor(period_id, base_date)
from_dt = (
    anchor.shift(weeks=FromOffset) if period_id == "WEEKLY" else anchor.shift(months=FromOffset)
).replace(day_or_week=FromOn, time=From)
```

---

## 5. Đề nghị SQL chuẩn hóa

> Để đồng bộ backend: **thêm các cột XaActiveOn, XaActiveAt, ... XaToOffset** vào bảng `loai_baocao`.


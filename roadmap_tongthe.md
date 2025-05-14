# ROADMAP TỔNG THỂ - DỰ ÁN HỆ THỐNG BÁO CÁO TIN TỨC (CẬP NHẬT 2025-04-27)

---

# 1. GIAI ĐOẠN 1: THIẾT KẾ LẠI BACKEND CƠ BẢN

## Bước 1.1: Hoàn thiện Model
- Xây dựng models:
  - `report_type.py`
  - `period.py`
  - `report.py`
  - `user.py`
  - `audit_log.py`

**Kiểm tra:**
- Tạo object thử nghiệm trong Python shell.
- Kiểm tra field đúng định nghĩa theo `Cautruc_logic.txt` và `spec_loaibaocao.txt`.

## Bước 1.2: Tạo Alembic Migration
- Tạo migration để tạo mới tất cả các bảng.

**Kiểm tra:**
- Chạy `alembic upgrade head`.
- Kiểm tra PostgreSQL đầy đủ các bảng và cột đúng.

---

# 2. GIAI ĐOẠN 2: XÂY DỰNG API BACKEND

## Bước 2.1: CRUD Loại Báo Cáo
- Endpoint: `/admin/loaibaocao`

## Bước 2.2: CRUD User
- Endpoint: `/admin/user`

## Bước 2.3: API cho Period
- `/period/active`
- `/period/create_auto`

## Bước 2.4: API cho Report
- `/report/upload`
- `/user/reports`

## Bước 2.5: API AuditLog
- `/admin/auditlogs`

**Kiểm tra:**
- Test trên Swagger UI từng API.
- Gửi request mẫu POST/GET/PUT/DELETE thành công.

---

# 3. GIAI ĐOẠN 3: THIẾT LẬP SCHEDULER

## Tích hợp APScheduler vào Backend
- Tự động:
  - Tạo và kích hoạt Period khi đến ActiveAt.
  - Hủy kích hoạt Period khi đến mốc hủy.

Chú ý tạo các log để dễ debug và kiểm thử bằng tay.

---

# 4. GIAI ĐOẠN 4: XÂY DỰNG FRONTEND

## Bước 4.1: Đăng nhập (LoginPage.jsx)
### 4.1.1: Đăng nhập cho tài khoản chi nhánh
- Nhập tài khoản/mật khẩu, checkbox ghi nhớ.
- Sau khi đăng nhập: UserDashboard.jsx.
### 4.1.2: Đăng nhập cho tài khoản quản trị
- Nhập tài khoản/mật khẩu, checkbox ghi nhớ.
- Sau khi đăng nhập: AdminDashboard.jsx.
**Kiểm tra:**
- Đăng nhập đúng role chuyển đúng giao diện.

## Bước 4.2: Trang UserDashboard.jsx
- Sidebar danh sách kỳ báo cáo.
- Nội dung chính: form gửi báo cáo.
- Header thông tin tài khoản, đổi mật khẩu, nhật ký gửi.

## Bước 4.3: Form đổi mật khẩu (ChangePassword.jsx)
- Đổi mật khẩu.

## Bước 4.4: Trang lịch sử gửi báo cáo (ReportHistory.jsx)
- Lọc theo kỳ, phân trang.

**Kiểm tra:**
- Đăng nhập, gửi báo cáo, xem lịch sử, đổi mật khẩu thành công.

## Bước 4.5: Trang AdminDashboard.jsx
- Sidebar:
  - Quản lý tài khoản chi nhánh (AdminAccounts.jsx)
  - Quản lý loại báo cáo (AdminLoaiBaoCao.jsx)
  - Quản lý kỳ báo cáo (AdminPeriods.jsx)
  - Quản lý báo cáo đã nhận (AdminReports.jsx)
  - Nhật ký thao tác (AdminAuditLog.jsx)

**Kiểm tra:**
- CRUD đầy đủ các bảng từ giao diện Admin.

---

# 5. GIAI ĐOẠN 5: KIỂM THỬ TỔNG THỂ

## Bước 5.1: Viết script kiểm thử Backend
- Test API upload báo cáo.
- Test API lịch sử báo cáo.
- Test API tự động tạo/huỷ kỳ.

**Kiểm tra:**
- Chạy script, tất cả test pass.

## Bước 5.2: Viết script kiểm thử Frontend
- Test đăng nhập, upload file, xem lịch sử.

**Kiểm tra:**
- Tất cả luồng tự động hoàn tất không lỗi.

---

# 6. GIAI ĐOẠN 6: HOÀN THIỆN

## Bước 6.1: Export Excel thống kê báo cáo
- Sử dụng `openpyxl` hoặc `pandas`.

**Kiểm tra:**
- Xuất file Excel, mở file đúng dữ liệu.

## Bước 6.2: Cập nhật README
- Hướng dẫn setup, chạy local, deploy.

**Kiểm tra:**
- Đọc README, thực hiện đầy đủ.

---

# GHI CHÚ
- Backend: FastAPI + PostgreSQL + APScheduler.
- Frontend: ReactJS + TailwindCSS + Vite.
- Storage: File local (có thể mở rộng S3).
- Xác thực: JWT OAuth2.
- Đặt tên biến, cột, bảng bằng tiếng Anh thống nhất.

# Kết thúc Roadmap


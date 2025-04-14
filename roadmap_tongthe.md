## 🛣️ Roadmap tổng thể dự án Hệ thống báo cáo tin tức

### Giai đoạn 1: Khởi tạo dự án & xây dựng cấu trúc thư mục cơ bản
- [ ] B1. Khởi tạo dự án backend FastAPI
  - [ ] Tạo cấu trúc thư mục `backend/app/`
  - [ ] Tạo file `main.py`, cấu hình route cơ bản
  - [ ] Cài đặt các thư viện: `fastapi`, `uvicorn`, `sqlalchemy`, `asyncpg`, `python-jose`, `passlib`, `pydantic`, `python-multipart`
  - [ ] Tạo `config.py` để quản lý cấu hình
  - [ ] Viết script kiểm thử: chạy được FastAPI với route `/ping`

- [ ] B2. Khởi tạo frontend bằng Vite + React + Tailwind
  - [ ] Cấu trúc thư mục `frontend/src`
  - [ ] Tạo các thư mục con: `pages/`, `components/`, `router/`, `services/`, `utils/`
  - [ ] Thiết lập layout chung: `App.jsx`, `main.jsx`, cấu hình routing cơ bản
  - [ ] Kiểm thử frontend hiển thị trang mẫu thành công

### Giai đoạn 2: Tài khoản và xác thực
- [ ] B3. Backend: Xây dựng tính năng xác thực JWT
  - [ ] Route: `/auth/login`, `/auth/register` (chỉ Admin), `/auth/me`
  - [ ] Mã hóa mật khẩu, tạo JWT Token, kiểm tra token
  - [ ] Tạo bảng `User` với các trường: username, password, tên chi nhánh, is_admin
  - [ ] Test đăng nhập, đăng ký, xác thực token

- [ ] B4. Frontend: Giao diện đăng nhập, xác thực
  - [ ] Giao diện login, lưu token vào localStorage
  - [ ] Middleware kiểm tra token khi gọi API

### Giai đoạn 3: Quản lý chi nhánh (tài khoản)
- [ ] B5. Backend: CRUD tài khoản chi nhánh
  - [ ] API: tạo, sửa, xóa, danh sách tài khoản
  - [ ] Liên kết bảng `User` với lịch sử báo cáo

- [ ] B6. Frontend: Giao diện quản lý tài khoản
  - [ ] Danh sách chi nhánh, form tạo/sửa/xóa tài khoản

### Giai đoạn 4: Hệ thống báo cáo
- [ ] B7. Backend: Upload báo cáo, lưu trữ file
  - [ ] API: `/report/upload`, `/report/history`, `/report/status`
  - [ ] Đổi tên file, tạo thư mục theo kỳ
  - [ ] Báo cáo ngày chia thành thư mục: `co_su_kien/`, `khong_su_kien/`
  - [ ] Ghi nhận thời gian gửi, trễ bao nhiêu giây
  - [ ] Tạo bảng `Report`

- [ ] B8. Frontend: Giao diện gửi báo cáo
  - [ ] Form chọn loại báo cáo, file upload, chọn sự kiện (nếu báo cáo ngày)
  - [ ] Đồng hồ đếm ngược thời hạn, hiển thị đúng/trễ (màu xanh/đỏ)

### Giai đoạn 5: Loại báo cáo và yêu cầu báo cáo
- [ ] B9. Backend: API quản lý loại báo cáo và yêu cầu
  - [ ] Tạo bảng `LoaiBaoCao` và `YeuCauBaoCao`
  - [ ] API tạo, sửa, xóa loại báo cáo
  - [ ] API tạo yêu cầu, phân phối tới tài khoản chi nhánh

- [ ] B10. Frontend: Quản lý loại báo cáo và hiển thị yêu cầu gửi
  - [ ] Admin: giao diện tạo loại và yêu cầu báo cáo
  - [ ] Chi nhánh: hiển thị nút báo cáo theo yêu cầu

### Giai đoạn 6: Thống kê báo cáo
- [ ] B11. Backend: Thống kê và export Excel
  - [ ] API `/admin/report/statistics`
  - [ ] Sử dụng pandas/openpyxl để xuất Excel với đầy đủ cột: tên đơn vị, thời gian, đúng hạn hay trễ, có sự kiện, tên file

- [ ] B12. Frontend: Giao diện thống kê cho admin
  - [ ] Bảng thống kê, lọc theo loại báo cáo, đơn vị, thời gian
  - [ ] Nút export Excel

### Giai đoạn 7: Tác vụ định kỳ & hoàn thiện
- [ ] B13. Cấu hình APScheduler hoặc Celery
  - [ ] Nhắc nhở qua email/tin nhắn khi gần hết hạn gửi báo cáo

- [ ] B14. Kiểm thử toàn hệ thống
  - [ ] Viết bộ test API cho tất cả route quan trọng
  - [ ] Test upload file, thống kê, xác thực báo cáo đúng/trễ

- [ ] B15. Triển khai production
  - [ ] Docker hóa backend và frontend
  - [ ] Triển khai PostgreSQL và lưu file lên S3 nếu cần
  - [ ] Triển khai server bằng Gunicorn + Nginx hoặc Uvicorn trực tiếp


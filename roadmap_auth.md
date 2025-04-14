## 🔐 Roadmap chi tiết: Xác thực & Quản lý tài khoản (JWT, Auth, User)

### Giai đoạn A1: Backend - Hệ thống xác thực và quản lý tài khoản (FastAPI)

#### A1.1. Cấu trúc backend cho xác thực
- [ ] Tạo `app/models/user.py`: model User gồm các trường
  - id (UUID), username (unique), hashed_password, branch_name, is_admin

- [ ] Tạo `app/schemas/user.py`: schema cho đăng ký, phản hồi, hiển thị
- [ ] Tạo `app/crud/user.py`: các hàm CRUD cho user
- [ ] Tạo `app/services/auth.py`: mã hóa mật khẩu, tạo & xác thực JWT
- [ ] Cập nhật `app/config.py`: thêm SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES

#### A1.2. Tạo route xác thực `/auth`
- [ ] `POST /auth/login`: trả về access token nếu đúng user/pass
- [ ] `POST /auth/register`: chỉ cho phép admin gọi
- [ ] `GET /auth/me`: trả lại thông tin user đang đăng nhập
- [ ] Gắn dependency xác thực (`Depends(get_current_user)`, kiểm tra `is_admin`)

#### A1.3. Middleware và bảo mật
- [ ] Tạo `app/dependencies/auth.py`: các hàm `get_current_user`, `get_current_admin`
- [ ] Tạo hàm xác thực từ JWT token gửi qua header `Authorization: Bearer`
- [ ] Gắn middleware xác thực vào các route cần quyền

#### A1.4. Kiểm thử backend
- [ ] Tạo script `tests/test_auth.py`:
  - Test login đúng/sai
  - Test tạo tài khoản admin/thường
  - Test truy cập /auth/me với và không có token


### Giai đoạn A2: Frontend - Đăng nhập và xác thực (ReactJS)

#### A2.1. Giao diện và lưu token
- [ ] Tạo trang `LoginPage.jsx`: form nhập username/password
- [ ] Gọi API `/auth/login`, lưu token vào localStorage nếu thành công
- [ ] Tạo context hoặc hook quản lý Auth (AuthContext)

#### A2.2. Middleware frontend
- [ ] Tạo `axiosInstance` tự động đính kèm Bearer token từ localStorage
- [ ] Chuyển hướng nếu chưa đăng nhập hoặc không có quyền
- [ ] Tạo HOC `withAuth()` để bảo vệ route cần quyền truy cập

#### A2.3. Kiểm thử frontend
- [ ] Kiểm tra: login → lưu token → gọi API `/auth/me`
- [ ] Test luồng đăng nhập, logout, bảo vệ route

### 🎯 Mục tiêu hoàn thành giai đoạn này:
- Người dùng có thể đăng nhập bằng tài khoản chi nhánh hoặc admin
- Admin có thể đăng ký tài khoản mới
- Hệ thống bảo vệ các route yêu cầu xác thực
- Token được gửi đi và kiểm tra đúng
- Giao diện frontend phản hồi đúng trạng thái đăng nhập


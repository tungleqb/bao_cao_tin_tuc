## 🚀 Roadmap chi tiết: Triển khai production (Deploy + Docker)

### Giai đoạn DEP1: Chuẩn bị môi trường

#### DEP1.1. Cấu hình môi trường server
- [ ] Cài đặt Python 3.10+, NodeJS, PostgreSQL, Docker, Nginx (nếu cần)
- [ ] Chuẩn bị thư mục lưu file báo cáo `static/reports`
- [ ] Thiết lập `.env` cho backend: DB URL, SECRET, JWT...

#### DEP1.2. Cài đặt Docker cho backend
- [ ] Tạo `Dockerfile` cho FastAPI
- [ ] Tạo `docker-compose.yml`:
  - Backend API (uvicorn)
  - PostgreSQL
  - Redis (nếu dùng Celery)

### Giai đoạn DEP2: Docker frontend và cấu hình Nginx

#### DEP2.1. Tạo Dockerfile frontend
- [ ] Build React bằng `Vite`
- [ ] Copy build vào container Nginx hoặc serve từ Node server

#### DEP2.2. Nginx cấu hình reverse proxy
- [ ] Route `/api/` tới FastAPI
- [ ] Route `/` tới frontend (index.html)
- [ ] Thiết lập HTTPS nếu dùng production

### Giai đoạn DEP3: Triển khai và test production

#### DEP3.1. Kiểm thử tích hợp
- [ ] Test toàn bộ API khi chạy qua Docker
- [ ] Test upload file, kiểm tra lưu vào đúng thư mục host

#### DEP3.2. Cấu hình giám sát
- [ ] Dùng `supervisor`, `systemd` hoặc Docker restart policy để đảm bảo app luôn chạy
- [ ] Gắn log về file hoặc hệ thống quản lý log (như Logrotate)

### 🎯 Mục tiêu hoàn thành:
- Triển khai trọn bộ hệ thống backend + frontend bằng Docker
- Có thể chạy độc lập trên server hoặc VPS
- Đảm bảo bảo mật cơ bản và phục hồi nhanh khi mất kết nối


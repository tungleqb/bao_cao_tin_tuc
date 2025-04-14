## 🌐 Roadmap chi tiết: Frontend hệ thống báo cáo (ReactJS + TailwindCSS + Vite)

### Giai đoạn F1: Cấu trúc dự án và khởi tạo giao diện chính

#### F1.1. Tạo cấu trúc thư mục
- [ ] `frontend/src/pages/`: chứa các trang như Login, Dashboard, UploadReport, History...
- [ ] `frontend/src/components/`: các thành phần UI như Navbar, CountdownClock, FileUpload...
- [ ] `frontend/src/router/`: định nghĩa các route chính của app
- [ ] `frontend/src/services/`: gọi API qua axios
- [ ] `frontend/src/utils/`: các hàm tiện ích như xử lý thời gian, hiển thị màu trạng thái...

#### F1.2. Tạo file gốc
- [ ] `App.jsx`: cấu trúc layout chung, navigation
- [ ] `main.jsx`: render App và config route
- [ ] `router.jsx`: định nghĩa các tuyến đường và route bảo vệ

#### F1.3. Thiết lập TailwindCSS
- [ ] Cài đặt Tailwind, cấu hình theme phù hợp màu xanh/đỏ trạng thái
- [ ] Thiết kế layout mobile first, responsive

### Giai đoạn F2: Các trang chính và giao diện người dùng

#### F2.1. Trang Login & Auth
- [ ] `LoginPage.jsx`: đăng nhập và lưu token
- [ ] Gọi `/auth/login`, chuyển route khi thành công

#### F2.2. Dashboard
- [ ] `Dashboard.jsx`: trang tổng quan sau đăng nhập
- [ ] Hiển thị tên chi nhánh, danh sách yêu cầu báo cáo, link đến upload

#### F2.3. Trang Upload Report
- [ ] `UploadReport.jsx`: form chọn loại báo cáo, upload file, chọn sự kiện (nếu là báo cáo ngày)
- [ ] Hiển thị deadline, màu trạng thái, đếm ngược
- [ ] Gọi API `/report/upload`

#### F2.4. Trang Lịch sử & Trạng thái báo cáo
- [ ] `HistoryReport.jsx`: bảng hiển thị các báo cáo đã gửi
- [ ] `StatusReport.jsx`: trạng thái đúng hạn / trễ / chưa gửi

### Giai đoạn F3: Giao diện admin

#### F3.1. Quản lý tài khoản chi nhánh
- [ ] `AdminAccounts.jsx`: danh sách user, form tạo/sửa/xoá

#### F3.2. Quản lý loại và yêu cầu báo cáo
- [ ] `AdminLoaiBaoCao.jsx`: CRUD loại báo cáo
- [ ] `AdminYeuCauBaoCao.jsx`: tạo yêu cầu gửi báo cáo tới đơn vị

#### F3.3. Thống kê và xuất Excel
- [ ] `AdminThongKeBaoCao.jsx`: bảng lọc, thống kê theo đơn vị, thời gian, loại báo cáo
- [ ] Nút xuất Excel

### 🎯 Mục tiêu hoàn thành frontend
- Giao diện người dùng đơn giản, rõ ràng
- Phản hồi màu và thời gian thực cho trạng thái báo cáo
- Giao diện quản trị đầy đủ, trực quan
- Kết nối API backend mượt mà, bảo vệ bằng JWT


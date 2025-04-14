## 🧑‍💼 Roadmap chi tiết: Quản trị hệ thống và quyền admin

### Giai đoạn ADM1: Backend - Tính năng quản trị

#### ADM1.1. Quản lý tài khoản chi nhánh
- [ ] API `/admin/user`:
  - `POST`: tạo tài khoản mới
  - `PUT`: cập nhật tên chi nhánh, mật khẩu
  - `DELETE`: xoá tài khoản
  - `GET`: danh sách tài khoản, lọc theo tên

- [ ] Chỉ cho phép admin gọi các route này (xác thực bằng `get_current_admin`)

#### ADM1.2. Quản lý loại báo cáo
- [ ] API `/admin/loaibaocao`:
  - CRUD loại báo cáo: tên loại, thời hạn, định kỳ (tuần, tháng...)

#### ADM1.3. Quản lý yêu cầu báo cáo
- [ ] API `/report/request`:
  - Tạo yêu cầu báo cáo đến danh sách chi nhánh cụ thể
  - Gắn loại báo cáo và kỳ hạn cụ thể

### Giai đoạn ADM2: Frontend - Giao diện quản trị

#### ADM2.1. Quản lý tài khoản chi nhánh
- [ ] Trang `AdminAccounts.jsx`
  - Bảng danh sách tài khoản
  - Modal thêm/sửa, xác thực xoá

#### ADM2.2. Quản lý loại báo cáo
- [ ] Trang `AdminLoaiBaoCao.jsx`
  - Tạo, sửa, xoá các loại báo cáo, xem kỳ hạn

#### ADM2.3. Quản lý yêu cầu báo cáo
- [ ] Trang `AdminYeuCauBaoCao.jsx`
  - Tạo yêu cầu cho từng loại báo cáo, gửi tới các đơn vị
  - Giao diện lịch sử các yêu cầu đã tạo

### 🎯 Mục tiêu
- Admin có giao diện đầy đủ để kiểm soát toàn bộ hệ thống
- Giao diện dễ thao tác với dữ liệu
- Các route admin được bảo vệ chặt chẽ


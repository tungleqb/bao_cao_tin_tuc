## 📁 Roadmap chi tiết: Quản lý và gửi báo cáo

### Giai đoạn B1: Backend - Upload, quản lý và phân loại báo cáo

#### B1.1. Tạo model và schema
- [ ] Tạo `models/report.py`:
  - id, loai_baocao_id, user_id, filename, filesize, has_event (bool), created_at

- [ ] Tạo `models/loai_baocao.py`: id, ten_loai, han_gui, dinh_ky

- [ ] Tạo `models/yeu_cau_baocao.py`: id, loai_baocao_id, user_ids[], dinh_ky

- [ ] Tạo schemas tương ứng trong `schemas/report.py`, `schemas/loai_baocao.py`, `schemas/yeu_cau.py`

#### B1.2. Xử lý upload file báo cáo
- [ ] API `/report/upload`:
  - Nhận file, tên loại báo cáo, trạng thái sự kiện (chỉ với báo cáo ngày)
  - Kiểm tra hạn gửi → ghi nhận đúng hạn / trễ + số giây
  - Đổi tên file theo định dạng `[Đơn vị]_[Loại báo cáo]_[Thời gian].ext`
  - Lưu vào thư mục `static/reports/<loai_baocao>/<ngay_ky>/`
  - Nếu là báo cáo ngày → chia vào thư mục `co_su_kien/` hoặc `khong_su_kien/`

#### B1.3. API liên quan
- [ ] `/report/history`: trả về lịch sử gửi của chi nhánh hiện tại
- [ ] `/report/status`: kiểm tra trạng thái gửi của chi nhánh từng kỳ
- [ ] `/admin/report/statistics`: thống kê toàn bộ báo cáo
- [ ] `/report/request`: tạo yêu cầu báo cáo tới các chi nhánh

#### B1.4. Kiểm thử backend báo cáo
- [ ] Test upload file với báo cáo ngày, thường
- [ ] Test đổi tên file và lưu đúng thư mục
- [ ] Test phân loại đúng vào co_su_kien / khong_su_kien
- [ ] Test báo cáo đúng hạn / trễ


### Giai đoạn B2: Frontend - Gửi báo cáo và hiển thị

#### B2.1. Giao diện gửi báo cáo
- [ ] Form chọn loại báo cáo
- [ ] Radiobox: "Có sự kiện đáng chú ý" / "Không có" (chỉ hiển thị nếu loại là "Báo cáo ngày")
- [ ] Đồng hồ đếm ngược đến hạn gửi báo cáo
- [ ] Giao diện hiện đúng hạn (nút xanh), trễ (nút đỏ)
- [ ] Upload file đính kèm (<= 50MB)

#### B2.2. Giao diện lịch sử và trạng thái
- [ ] Trang `LichSuBaoCao.jsx`: hiển thị các báo cáo đã gửi + thời gian + đúng hạn / trễ
- [ ] Trang `TrangThaiBaoCao.jsx`: hiển thị các kỳ chưa gửi, sắp hết hạn

#### B2.3. Admin: thống kê và yêu cầu báo cáo
- [ ] Trang `ThongKeBaoCao.jsx`: bảng lọc, nút export Excel
- [ ] Trang `YeuCauBaoCao.jsx`: tạo yêu cầu theo loại và chi nhánh

### 🎯 Mục tiêu hoàn thành giai đoạn này:
- Chi nhánh có thể gửi đúng hạn/trễ
- Hệ thống tự phân loại và lưu file theo chuẩn
- Admin thống kê được đầy đủ, tải về Excel
- Giao diện hiển thị dễ hiểu và phản hồi đúng trạng thái báo cáo


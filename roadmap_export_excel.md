## 📊 Roadmap chi tiết: Thống kê và xuất Excel

### Giai đoạn EX1: Backend - Tạo báo cáo thống kê

#### EX1.1. API thống kê và phân tích
- [ ] API `/admin/report/statistics`:
  - Trả về danh sách báo cáo theo bộ lọc: loại báo cáo, đơn vị, thời gian, đúng hạn hay không
  - Bao gồm các trường:
    - STT, Tên đơn vị, Thời gian gửi, Trễ bao nhiêu giây, Có sự kiện hay không, Tên file

#### EX1.2. Xuất Excel từ backend
- [ ] Sử dụng `pandas` hoặc `openpyxl` để tạo file Excel
- [ ] Tạo tên file theo định dạng: `thongke_<ngay>.xlsx`
- [ ] Định dạng cột rõ ràng, tự động wrap text nếu cần
- [ ] Tải file từ response API dưới dạng `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

### Giai đoạn EX2: Frontend - Giao diện thống kê

#### EX2.1. Hiển thị bảng thống kê
- [ ] Trang `AdminThongKeBaoCao.jsx`
  - Bảng thống kê báo cáo: STT, đơn vị, thời gian gửi, đúng hạn/trễ...
  - Có thể lọc theo đơn vị, thời gian, loại báo cáo

#### EX2.2. Xuất file Excel
- [ ] Nút “Xuất Excel” → gọi API tải file Excel về
- [ ] Hiển thị thông báo tải về thành công, lỗi nếu có

### 🎯 Mục tiêu hoàn thành:
- Admin có thể xem và tải thống kê chi tiết dưới dạng bảng và file Excel
- File Excel hiển thị rõ ràng, dễ in, lưu trữ


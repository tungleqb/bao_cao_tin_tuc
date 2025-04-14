## ⏰ Roadmap chi tiết: Nhắc báo cáo định kỳ (Scheduler)

### Giai đoạn SCH1: Backend - Cài đặt định kỳ và nhắc hạn báo cáo

#### SCH1.1. Cấu hình định kỳ gửi báo cáo
- [ ] Mỗi loại báo cáo sẽ có trường `dinh_ky` (tuần, tháng, quý, năm... hoặc 0 nếu không lặp lại)
- [ ] Tự động tạo yêu cầu báo cáo định kỳ dựa trên thông tin loại báo cáo
- [ ] Ghi nhận kỳ tiếp theo khi đến hạn

#### SCH1.2. Gửi thông báo nhắc nhở
- [ ] Tích hợp `APScheduler` hoặc `Celery` + Redis
- [ ] Kiểm tra các đơn vị chưa gửi → gửi thông báo (email, webhook, console log)
- [ ] Thời điểm nhắc: trước hạn 1h, 1 ngày, tùy loại báo cáo

#### SCH1.3. Theo dõi tiến độ định kỳ
- [ ] API `/admin/report/next-deadline` hoặc cron xử lý → cập nhật trạng thái gửi
- [ ] Tự động gắn trạng thái đúng hạn / trễ khi đã qua kỳ hạn

### Giai đoạn SCH2: Kiểm thử Scheduler

#### SCH2.1. Test logic tạo báo cáo định kỳ
- [ ] Test loại báo cáo định kỳ tuần, tháng, năm → tự tạo yêu cầu đúng thời điểm

#### SCH2.2. Test gửi thông báo nhắc
- [ ] Đơn vị chưa gửi → được nhắc đúng thời điểm
- [ ] Đơn vị đã gửi → không nhắc

### 🎯 Mục tiêu
- Hệ thống hoạt động ổn định, tự sinh yêu cầu theo định kỳ
- Nhắc chi nhánh đúng thời điểm, không gây phiền phức
- Trạng thái báo cáo được ghi nhận tự động, chính xác


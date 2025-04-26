**ROADMAP TONG THE VA CHI TIET - DU AN BAO CAO TIN TUC (CAP NHAT MOI)**

# 1. GIAI DOAN 1: CAP NHAT CO SO DU LIEU

## Buoc 1.1: Tao model Period va update model Report
- Tao file `backend/app/models/period.py`.
- Cap nhat file `backend/app/models/report.py` de dung theo format moi (Sender, SendID, PeriodID, ...).

**Kiem tra:**
- Khoi tao doi tuong Period bang tay trong Python shell.
- Khoi tao doi tuong Report moi voi du lieu day du.

## Buoc 1.2: Tao Alembic Migration
- Sinh file migration tu dong: `alembic revision --autogenerate -m "create period table and update report table"`
- Chay `alembic upgrade head`.

**Kiem tra:**
- Kiem tra PostgreSQL: xuat hien bang `periods` va update bang `reports`.

---

# 2. GIAI DOAN 2: CAP NHAT BACKEND API

## Buoc 2.1: CRUD cho Period
- Tao file `backend/app/routers/period.py`.
- Tao schema `backend/app/schemas/period.py`.
- Tao route: GET, POST, PUT, DELETE Period.

**Kiem tra:**
- Dung Swagger UI test: tao, cap nhat, xoa 1 Period thanh cong.

## Buoc 2.2: APIs Upload Report theo Period
- Cap nhat API `/report/upload`:
  - Nhan thong tin PeriodID.
  - Tinh toan LateSeconds.
  - Luu file vao folder cua Period.
  - Sinh checksum Blake3 cho file.

**Kiem tra:**
- Upload file tren Swagger UI: kiem tra file duoc luu dung thu muc, dung dinh dang Report.

## Buoc 2.3: APIs lay lich su bao cao user
- Them API `/user/reports`:
  - Lay danh sach cac bao cao da gui cua user hien tai.

**Kiem tra:**
- Test API lay danh sach bao cao cua user trong Swagger UI.

## Buoc 2.4: APIs Periods dang kich hoat
- Them API `/period/active`:
  - Tra ve danh sach cac ky dang active cua user hien tai.

**Kiem tra:**
- Test API tra ve danh sach dung ky dang kich hoat.

---

# 3. GIAI DOAN 3: THEM TU DONG HOA (SCHEDULER)

## Buoc 3.1: Tich hop APScheduler
- Cai dat APScheduler vao FastAPI.
- Dinh nghia job:
  - Tu dong tao Period khi den ActiveAt.
  - Tu dong huy Period khi den DeactiveAt.

**Kiem tra:**
- Tao mot Period co thoi diem ActiveAt trong 2 phut toi.
- Cho he thong tu kich hoat va huy Period do.

---

# 4. GIAI DOAN 4: CAP NHAT FRONTEND

## Buoc 4.1: Cap nhat luong dang nhap
- Neu user la Admin -> vao dashboard admin.
- Neu user la chi nhanh -> vao UserHomePage.

**Kiem tra:**
- Dang nhap voi 2 loai user: chuyen dung giao dien tuong ung.

## Buoc 4.2: Xay dung trang UserHomePage
- Sidebar trai: danh sach Period dang active.
- Noi dung chinh: giao dien Upload Report theo Period.
- Header: thong tin user, menu nho.

**Kiem tra:**
- Dang nhap, xem danh sach ky, upload bao cao moi, kiem tra file upload.

## Buoc 4.3: Trang lich su bao cao (ReportHistory)
- Danh sach bao cao da gui.
- Loc theo Period.
- Phan trang neu du lieu lon.

**Kiem tra:**
- Vao trang xem lich su bao cao, loc du lieu.

## Buoc 4.4: Admin quan ly Kỳ báo cáo (AdminPeriods.jsx)
- Giao dien tao, cap nhat, xoa, kich hoat ky bao cao.

**Kiem tra:**
- Tao ky moi, sua ky, xoa ky.

---

# 5. GIAI DOAN 5: KIEM THU TONG THE

## Buoc 5.1: Viet script kiem thu Backend
- Test API upload bao cao.
- Test API lich su bao cao.
- Test API tu dong tao/huy Period.

**Kiem tra:**
- Chay script -> tat ca test pass.

## Buoc 5.2: Viet script kiem thu Frontend
- Test tu dong login, upload file, xem lich su.

**Kiem tra:**
- Tat ca luong tu dong hoan tat khong loi.

---

# 6. GIAI DOAN 6: HOAN THIEN

## Buoc 6.1: Export Excel thong ke bao cao
- Chuc nang xuat thong ke ky bao cao ra file Excel.

**Kiem tra:**
- Xuat file Excel, mo file dung du lieu.

## Buoc 6.2: Cap nhat README, huong dan su dung
- Cap nhat tai lieu README.md.
- Bo sung cac API moi.

**Kiem tra:**
- Mo README, doc day du cac buoc huong dan.

---

# Ket thuc Roadmap


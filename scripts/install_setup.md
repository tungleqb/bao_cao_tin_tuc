# Bước 1: Tạo môi trường ảo
cd backend
python -m venv venv

# Bước 2: Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Bước 3: Cài thư viện vào môi trường ảo
pip install -r requirements.txt

# Bước 4: Chạy server
bash run_test_ping.sh


# Cài nvm nếu chưa có
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc  # hoặc ~/.zshrc nếu dùng zsh

# Cài node phiên bản mới (ví dụ v20)
nvm install 20
nvm use 20

# Kiểm tra lại
node -v
npm -v


# Bắt đầu từ thư mục frontend
cd ~/bao_cao_tin_tuc/frontend

# Khởi tạo dự án Vite (React)
npm create vite@latest . -- --template react

# Cài đặt các phụ thuộc

## Cài đặt & chạy:
cd frontend
npm install
npm run dev

Truy cập: http://localhost:5173


 Kế hoạch chuyển đổi sang PostgreSQL:
🔧 Bước 1: Cấu hình kết nối và khởi tạo database
Sử dụng config.py với DATABASE_URL

Tạo engine + session (SQLAlchemy async)

🗃️ Bước 2: Tạo bảng User trong models/user.py (đã có)
Bao gồm: id, username, hashed_password, ten_chi_nhanh, is_admin

💾 Bước 3: Tạo file database.py để quản lý session
Tạo SessionLocal, Base, get_db()

🔁 Bước 4: Sửa auth.py:
Thay fake_users_db bằng thao tác thật trên database (dùng session)

🧪 Bước 5: Khởi tạo bảng (nếu chưa có)
Chạy Base.metadata.create_all(bind=engine) (hoặc migrate sau này)

sudo apt install postgresql postgresql-contrib -y

✅ Hướng dẫn chạy:
1. Tạo PostgreSQL và database thực (nếu chưa có):
sudo service postgresql start
sudo -u postgres psql
CREATE DATABASE baocao;
CREATE USER report_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE baocao TO report_user;
\q
2. Sửa .env hoặc config.py:
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/baocao"
3. Cài thư viện và chạy:
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload
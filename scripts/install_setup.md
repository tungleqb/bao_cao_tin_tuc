# Bước 1: Tạo môi trường ảo
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


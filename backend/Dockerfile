FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LOG_LEVEL=info

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip \
    nano \
 && rm -rf /var/lib/apt/lists/*
# ✅ THAY ĐỔI: dùng /backend thay vì /app
WORKDIR /backend

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# ✅ copy toàn bộ mã vào /backend
COPY . .

# ✅ đảm bảo có quyền thực thi
RUN chmod +x start.sh

EXPOSE 8000

# ✅ chạy start.sh tại WORKDIR=/backend
CMD ["./start.sh"]


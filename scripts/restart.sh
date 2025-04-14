#!/bin/bash

echo "🚦 Đang dừng Docker containers cũ..."
docker-compose down --volumes

echo "🔄 Đang build lại và khởi động containers..."
docker-compose up -d --build

echo "✅ Đã khởi động lại thành công!"

echo "📦 Danh sách containers đang chạy:"
docker ps

echo "💡 Truy cập Frontend: http://localhost:5173"
echo "💡 Truy cập Backend Docs (FastAPI): http://localhost:8000/docs"


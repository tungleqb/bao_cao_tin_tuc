#!/bin/bash

CERT_DIR="/cert"
CERT_KEY="$CERT_DIR/server.key"
CERT_CRT="$CERT_DIR/server.crt"

# Nếu chưa có chứng chỉ, tạo mới
if [ ! -f "$CERT_KEY" ] || [ ! -f "$CERT_CRT" ]; then
    echo "🔐 Generating self-signed certificate..."
    mkdir -p "$CERT_DIR"

    openssl req -x509 -nodes -days 3650 \
        -newkey rsa:2048 \
        -keyout "$CERT_KEY" \
        -out "$CERT_CRT" \
        -subj "/CN=${CERT_HOST:-localhost}"
    
    echo "✅ Certificate created for ${CERT_HOST:-localhost}"
else
    echo "✔️ Using existing certificate"
fi

# Khởi chạy uvicorn
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --ssl-keyfile "$CERT_KEY" \
    --ssl-certfile "$CERT_CRT"

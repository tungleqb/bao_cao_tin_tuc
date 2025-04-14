cd ~/tramproxy2/backend
source env/bin/activate  # nếu dùng môi trường ảo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Hướng dẫn migrate Alembic

1. Kích hoạt venv:
.\venv\Scripts\Activate.ps1

2. Xoá migration lỗi (nếu có):
del backend\alembic\versions\*.py

3. Sinh file migration mới:
alembic revision --autogenerate -m "init database schema"

4. Nâng cấp database:
alembic upgrade head

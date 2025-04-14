Step 3
#alembic revision --autogenerate -m "init user table"
#alembic upgrade head

Dùng pip trong môi trường ảo (env trong wsl) env
Kích hoạt venv (nếu có):

sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

sudo apt install python3.12 python3.12-venv python3.12-dev -y

python3.12 --version

python3.12 -m venv venv
source venv/bin/activate

(deactivate)

pip install -r requirements.txt

Cấu hình localhost khi chạy trên WSL
# .env (dành cho local WSL)
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/bridge_db
trong alembic.ini
Hoặc trong .env / database.py cũng nên dùng localhost nếu bạn không dùng Docker.

sudo apt update
sudo apt install postgresql postgresql-contrib -y

sudo service postgresql start

sudo -u postgres psql

CREATE DATABASE bridge_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE bridge_db TO postgres;
\q

sudo -u postgres psql

ALTER USER postgres WITH PASSWORD 'postgres';
\q

target_metadata = Base.metadata
trong alembic/env.py

alembic revision --autogenerate -m "init user table"
alembic upgrade head

✅ Tạo migration thành công với Alembic
✅ Chạy upgrade và tạo bảng users trong PostgreSQL thành công


Liên quan đến EmailStr
pip install pydantic[email]


Phục vụ test
pip install fastapi pytest pytest-asyncio httpx[http2] jose

pytest-asyncio hoặc anyio tự động thử chạy test với backend trio, nhưng bạn chưa cài nó.
pip install trio

pip uninstall pytest-anyio -y
pip install pytest-asyncio


Cập nhật cấu trúc Alembic, CHÚ Ý .gitignore để tránh mất khi pull
alembic revision --autogenerate -m "Add APIKey model"

alembic upgrade head

✅ Cách kiểm tra nhanh:
Chạy lệnh sau trong shell PostgreSQL để kiểm tra:

bash
Sao chép
Chỉnh sửa
psql -U postgres -d bridge_db -c "\dt"
Kết quả mong đợi:

plaintext
Sao chép
Chỉnh sửa
                 List of relations
 Schema |       Name       | Type  |  Owner
--------+------------------+-------+----------
 public | users            | table | postgres
 public | api_keys         | table | postgres  ← PHẢI CÓ

sudo -u postgres psql -d bridge_db -c "\dt"

pip install asyncpg

pip install pydantic-settings
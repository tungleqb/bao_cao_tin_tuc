from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://report_user:password@localhost:5444/baocao")
engine = create_engine(DATABASE_URL)

metadata = MetaData()
metadata.reflect(bind=engine)

print("📋 Danh sách cột theo từng bảng:\n")
for table_name, table in metadata.tables.items():
    print(f"🗂️ {table_name}:")
    for column in table.columns:
        print(f"   - {column.name} ({column.type})")
    print()

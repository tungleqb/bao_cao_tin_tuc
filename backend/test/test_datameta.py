# file test_metadata.py
from database import Base
print(Base.metadata.tables.keys())

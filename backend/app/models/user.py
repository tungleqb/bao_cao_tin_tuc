from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    time_created = Column(DateTime, nullable=True)
    avatar = Column(String, nullable=True)
    level = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)

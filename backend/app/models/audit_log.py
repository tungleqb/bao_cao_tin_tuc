from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    model = Column(String, nullable=False)
    model_id = Column(String, nullable=False)  # ✅ đổi từ Integer sang String
    details = Column(String)
    timestamp = Column(DateTime, nullable=False)



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    loai_baocao_id = Column(Integer, ForeignKey("loai_baocao.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    filesize = Column(Integer)
    has_event = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_late = Column(Boolean, default=False)
    late_seconds = Column(Integer, default=0)

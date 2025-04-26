from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Period(Base):
    __tablename__ = "periods"

    TYPE = Column(String, nullable=False)  # ID của loại báo cáo
    ID = Column(String, primary_key=True, index=True)  # <TYPE>_<ActiveAt>
    Name = Column(String, nullable=False)
    ActiveAt = Column(DateTime(timezone=True), nullable=False)
    DeactiveAt = Column(DateTime(timezone=True), nullable=False)
    StartAt = Column(DateTime(timezone=True), nullable=False)
    EndAt = Column(DateTime(timezone=True), nullable=False)
    FromAt = Column(DateTime(timezone=True), nullable=False)
    ToAt = Column(DateTime(timezone=True), nullable=False)
    Killer = Column(String, nullable=False)  # Auto / Admin
    Status = Column(String, nullable=False)  # Active / Deactive
    FolderPath = Column(String, nullable=True)  # Đường dẫn thư mục lưu báo cáo

    reports = relationship("Report", back_populates="period")

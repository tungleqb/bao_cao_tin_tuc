from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Report(Base):
    __tablename__ = "reports"

    ID = Column(String, primary_key=True, index=True)
    Sender = Column(String, nullable=False)
    SendID = Column(Integer, nullable=False)
    PeriodID = Column(String, ForeignKey("periods.ID"), nullable=False)
    ReportTypeID = Column(String, nullable=False)
    ReportPeriodName = Column(String, nullable=False)
    Blake3sum = Column(String, nullable=False)
    FilePath = Column(String, nullable=False)
    FileName = Column(String, nullable=False)
    OriFileName = Column(String, nullable=False)
    FileSize = Column(Integer, nullable=False)
    SentAt = Column(DateTime(timezone=True), nullable=False)
    Comment = Column(String, nullable=True)
    HasEvent = Column(Boolean, default=False)
    LateSeconds = Column(Integer, default=0)

    period = relationship("Period", back_populates="reports")

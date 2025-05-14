from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Period(Base):
    __tablename__ = "periods"

    TYPE = Column(String, nullable=False)
    ID = Column(String, primary_key=True, index=True)
    Name = Column(String, nullable=False)

    ActiveAt = Column(DateTime(timezone=True), nullable=False)
    DeactiveAt = Column(DateTime(timezone=True), nullable=False)
    StartAt = Column(DateTime(timezone=True), nullable=False)
    EndAt = Column(DateTime(timezone=True), nullable=False)
    FromAt = Column(DateTime(timezone=True), nullable=False)
    ToAt = Column(DateTime(timezone=True), nullable=False)

    XaActiveAt = Column(DateTime(timezone=True), nullable=True)
    XaDeactiveAt = Column(DateTime(timezone=True), nullable=True)
    XaStartAt = Column(DateTime(timezone=True), nullable=True)
    XaEndAt = Column(DateTime(timezone=True), nullable=True)
    XaFromAt = Column(DateTime(timezone=True), nullable=True)
    XaToAt = Column(DateTime(timezone=True), nullable=True)

    Status = Column(String, nullable=False)
    XaStatus = Column(String, nullable=True)

    Killer = Column(String, nullable=False)
    FolderPath = Column(String, nullable=True)

    reports = relationship("Report", back_populates="period")

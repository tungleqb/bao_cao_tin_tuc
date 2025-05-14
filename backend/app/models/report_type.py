from sqlalchemy import Column, String, Integer, Time, DateTime, CheckConstraint
from ..database import Base

class ReportType(Base):
    __tablename__ = "report_types"
    __table_args__ = (
        CheckConstraint('"Period_ID" IN (\'DAILY\',\'WEEKLY\',\'MONTHLY\',\'NONE\')', name='period_id_check'),
    )

    ID = Column(String, primary_key=True, index=True)
    DateCreated = Column(DateTime, nullable=False)
    Name = Column(String, nullable=False)
    Period_ID = Column(String, nullable=False)  # DAILY, WEEKLY, MONTHLY, NONE

    ActiveOffset = Column(Integer, default=0)
    ActiveOn = Column(Integer, default=0)
    ActiveAt = Column(Time, nullable=False)

    DeactiveOffset = Column(Integer, default=0)
    DeactiveOn = Column(Integer, default=0)
    DeactiveAt = Column(Time, nullable=False)

    StartOffset = Column(Integer, default=0)
    StartOn = Column(Integer, default=0)
    StartAt = Column(Time, nullable=False)

    EndOffset = Column(Integer, default=0)
    EndOn = Column(Integer, default=0)
    EndAt = Column(Time, nullable=False)

    FromOffset = Column(Integer, default=0)
    FromOn = Column(Integer, default=0)
    From = Column(Time, nullable=False)

    ToOffset = Column(Integer, default=0)
    ToOn = Column(Integer, default=0)
    To = Column(Time, nullable=False)

    XaActiveOffset = Column(Integer, default=0)
    XaActiveOn = Column(Integer, default=0)
    XaActiveAt = Column(Time, nullable=True)

    XaDeactiveOffset = Column(Integer, default=0)
    XaDeactiveOn = Column(Integer, default=0)
    XaDeactiveAt = Column(Time, nullable=True)

    XaStartOffset = Column(Integer, default=0)
    XaStartOn = Column(Integer, default=0)
    XaStartAt = Column(Time, nullable=True)

    XaEndOffset = Column(Integer, default=0)
    XaEndOn = Column(Integer, default=0)
    XaEndAt = Column(Time, nullable=True)

    XaFromOffset = Column(Integer, default=0)
    XaFromOn = Column(Integer, default=0)
    XaFromAt = Column(Time, nullable=True)

    XaToOffset = Column(Integer, default=0)
    XaToOn = Column(Integer, default=0)
    XaToAt = Column(Time, nullable=True)

    DocExtList = Column(String, default=".doc .docx .pdf .bm2 .jpg .xlsx .xls")
    MaxSize = Column(String, default="100MB")
    NextAt = Column(DateTime, nullable=True)
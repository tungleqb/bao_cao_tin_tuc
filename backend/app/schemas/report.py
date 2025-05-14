# backend/app/schemas/report.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict

class ReportBase(BaseModel):
    Sender: str
    SendID: int
    PeriodID: str
    ReportTypeID: str
    ReportPeriodName: str
    Blake3sum: str
    FilePath: str
    FileName: str
    OriFileName: str
    FileSize: int
    SentAt: datetime
    Comment: Optional[str] = None
    HasEvent: Optional[bool] = False
    LateSeconds: Optional[int] = 0

class ReportCreate(ReportBase):
    ID: str

class ReportUpdate(BaseModel):
    Comment: Optional[str] = None
    HasEvent: Optional[bool] = None

class ReportOut(ReportCreate):
    model_config = ConfigDict(from_attributes=True)

class ReportStatus(BaseModel):
    Status: str  # "sent" hoặc "not_sent"
    Blake3sum: Optional[str] = None
    SentAt: Optional[datetime] = None
    LateSeconds: Optional[int] = None
    HasEvent: Optional[bool] = None
    OriFileName: Optional[str] = None
    ID: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)



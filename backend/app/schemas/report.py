
from pydantic import BaseModel
from datetime import datetime

class ReportOut(BaseModel):
    id: int
    filename: str
    filesize: int
    created_at: datetime
    is_late: bool
    late_seconds: int
    has_event: bool

    class Config:
        from_attributes = True

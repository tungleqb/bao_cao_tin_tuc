from pydantic import BaseModel
from datetime import datetime

class AuditLogOut(BaseModel):
    id: int
    action: str
    model: str
    model_id: int | None
    timestamp: datetime
    details: str | None

    class Config:
        from_attributes = True

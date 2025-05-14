# backend/app/schemas/audit_log.py

from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict

class AuditLogBase(BaseModel):
    user_id: int
    action: str
    model: str
    model_id: str | None = None
    details: str | None = None
    timestamp: datetime

class AuditLogCreate(BaseModel):
    user_id: int
    action: str
    model: str
    model_id: str  # ✅ CHỈNH từ int → str
    details: str
    timestamp: datetime


class AuditLogOut(AuditLogBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

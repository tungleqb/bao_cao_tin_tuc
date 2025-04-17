from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.audit_log import AuditLog
from ..schemas.audit_log import AuditLogOut
from ..database import get_db
from ..dependencies.auth import get_current_admin

router = APIRouter()

@router.get("/logs", response_model=list[AuditLogOut])
async def get_logs(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()))
    return result.scalars().all()

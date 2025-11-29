from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import audit_log as crud
from ..schemas.audit_log import AuditLogOut
from ..dependencies.auth import get_current_admin
from ..schemas.user import UserOut

router = APIRouter(
    prefix="/admin/auditlogs",
    tags=["Admin-AuditLog"]
)

@router.get("", response_model=list[AuditLogOut])
async def read_audit_logs(db: AsyncSession = Depends(get_db), user: UserOut = Depends(get_current_admin)):
    logs = None
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        logs = await crud.get_audit_logs(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching audit logs: {str(e)}")
        return logs
    return logs

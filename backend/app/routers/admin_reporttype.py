from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import report_type as schema
from ..crud import report_type as crud
from ..dependencies.auth import get_current_admin
from ..database import get_db
from ..schemas.audit_log import AuditLogCreate
from ..crud import audit_log as crud_audit_log
from datetime import datetime, timezone

router = APIRouter(prefix="/admin/reporttype", tags=["Admin-reporttype"])

@router.post("", response_model=schema.ReportTypeOut)
async def create(report_type_in: schema.ReportTypeCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action=f"/admin/reporttype",
            model="post",
            model_id=user.username,
            details=f"Create {report_type_in.Name}",
            timestamp=now.replace(tzinfo=None)
        ))
        return await crud.create_report_type(db, report_type_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating report type: {str(e)}")

@router.get("", response_model=list[schema.ReportTypeOut])
async def read_all(db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        return await crud.get_report_types(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching report types: {str(e)}")   

@router.put("/{id}", response_model=schema.ReportTypeOut)
async def update(id: str, report_type_in: schema.ReportTypeUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        old = await crud.get_report_type(db, id)
        if not old:
            raise HTTPException(status_code=404, detail="ReportType not found")
        await crud.update_report_type(db, id, report_type_in)
        updated = await crud.get_report_type(db, id)

        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action=f"/admin/reporttype/{id}",
            model="put",
            model_id=user.username,
            details=f"Update {report_type_in.Name}",
            timestamp=now.replace(tzinfo=None)
        ))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating report type: {str(e)}")

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        old = await crud.get_report_type(db, id)
        if not old:
            raise HTTPException(status_code=404, detail="ReportType not found")
        await crud.delete_report_type(db, id)
        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action=f"/admin/reporttype/{id}",
            model="put",
            model_id=user.username,
            details=f"Delete report type {id}",
            timestamp=now.replace(tzinfo=None)
        ))
        return {"msg": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting report type: {str(e)}")

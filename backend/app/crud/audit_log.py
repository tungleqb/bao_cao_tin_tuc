# backend/app/crud/audit_log.py

from sqlalchemy.ext.asyncio import AsyncSession
from ..models.audit_log import AuditLog
from ..schemas.audit_log import AuditLogCreate
from sqlalchemy.future import select
from sqlalchemy import update, delete

async def create_audit_log(db: AsyncSession, audit_log_in: AuditLogCreate):
    try:
        audit_log = AuditLog(**audit_log_in.model_dump())
        db.add(audit_log)
        await db.commit()
        await db.refresh(audit_log)
        return audit_log
    except Exception as e:
        print(f"❌ Error creating audit log: {e}")
        await db.rollback()
        return None
    
async def get_audit_logs(db: AsyncSession):
    try:
        result = await db.execute(select(AuditLog))
        return result.scalars().all()
    except Exception as e:
        print(f"❌ Error fetching audit logs: {e}")
        return []

async def get_audit_log(db: AsyncSession, audit_log_id: int):
    try:
        result = await db.execute(select(AuditLog).where(AuditLog.id == audit_log_id))
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"❌ Error fetching audit log with ID {audit_log_id}: {e}")
        return None

async def delete_audit_log(db: AsyncSession, audit_log_id: int):
    try:
        stmt = delete(AuditLog).where(AuditLog.id == audit_log_id)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error deleting audit log with ID {audit_log_id}: {e}")
        await db.rollback()
        return False
    return True

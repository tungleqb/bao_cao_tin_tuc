from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException
from ..models.report_type import ReportType
from ..schemas.report_type import ReportTypeCreate, ReportTypeUpdate
from datetime import datetime
from uuid import uuid4

async def create_report_type(db: AsyncSession, report_type_in: ReportTypeCreate):
    try:
        result = await db.execute(select(ReportType).where(ReportType.Name == report_type_in.Name))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="ReportType Name already exists")

        # ReportType(**report_type_in.dict()) is now validated with `Literal` for Period_ID
        id = f"{report_type_in.Period_ID}_{uuid4().hex[:8].upper()}"
        date_created = datetime.now()
        next_at = datetime.now()

        report_type_data = report_type_in.model_dump()
        report_type = ReportType(
            ID=id,
            DateCreated=date_created,
            NextAt=next_at,
            **report_type_data
        )
        db.add(report_type)
        await db.commit()
        await db.refresh(report_type)
        return report_type
    except Exception as e:  
        print(f"❌ Error creating report type: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_report_types(db: AsyncSession):
    try:
        result = await db.execute(select(ReportType))
        return result.scalars().all()
    except Exception as e:  
        print(f"❌ Error fetching report types: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_report_type(db: AsyncSession, report_type_id: str):
    try:
        result = await db.execute(select(ReportType).where(ReportType.ID == report_type_id))
        return result.scalar_one_or_none()
    except Exception as e:  
        print(f"❌ Error fetching report type with ID {report_type_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_report_type(db: AsyncSession, report_type_id: str, report_type_in: ReportTypeUpdate):
    try:
        stmt = update(ReportType).where(ReportType.ID == report_type_id).values(**report_type_in.model_dump(exclude_unset=True))
        await db.execute(stmt)
        await db.commit()
    except Exception as e:   
        print(f"❌ Error updating report type with ID {report_type_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_report_type(db: AsyncSession, report_type_id: str):
    try:
        stmt = delete(ReportType).where(ReportType.ID == report_type_id)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:   
        print(f"❌ Error deleting report type with ID {report_type_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

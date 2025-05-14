# backend/app/crud/period.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException
from ..models.period import Period
from ..schemas.period import PeriodCreate, PeriodUpdate
from datetime import datetime

async def create_period(db: AsyncSession, period_in: PeriodCreate):
    try:
        result = await db.execute(select(Period).where(Period.ID == period_in.ID))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Period ID already exists")

        period = Period(**period_in.model_dump())
        db.add(period)
        await db.commit()
        await db.refresh(period)
        return period
    except Exception as e:
        print(f"❌ Error creating period: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_periods(db: AsyncSession):
    try:
        result = await db.execute(select(Period))
        return result.scalars().all()
    except Exception as e:
        print(f"❌ Error fetching periods: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_period(db: AsyncSession, period_id: str):
    try:
        result = await db.execute(select(Period).where(Period.ID == period_id))
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"❌ Error fetching period with ID {period_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_period(db: AsyncSession, period_id: str, period_in: PeriodUpdate):
    try:
        stmt = update(Period).where(Period.ID == period_id).values(**period_in.model_dump(exclude_unset=True))
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error updating period with ID {period_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_period(db: AsyncSession, period_id: str):
    try:
        stmt = delete(Period).where(Period.ID == period_id)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error deleting period with ID {period_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_all_periods(db: AsyncSession):
    try:
        result = await db.execute(select(Period))
        return result.scalars().all()
    except Exception as e:  
        print(f"❌ Error fetching all periods: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_period_status(db: AsyncSession, period_id: str, status: str = None, xa_status: str = None):
    try:
        result = await db.execute(select(Period).where(Period.ID == period_id))
        period = result.scalar_one_or_none()
        if period:
            if status is not None:
                period.Status = status
            if xa_status is not None:
                period.XaStatus = xa_status
            await db.commit()
            await db.refresh(period)
        return period
    except Exception as e:  
        print(f"❌ Error updating status for period with ID {period_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
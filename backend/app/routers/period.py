import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from ..schemas.period import PeriodCreate, PeriodUpdate, PeriodOut
from ..models.period import Period
from ..crud import period as crud_period
from ..database import get_db
from ..dependencies.auth import get_current_user
from ..schemas.user import UserOut

router = APIRouter(prefix="/period", tags=["Period"])

@router.post("/", response_model=PeriodOut)
async def create_period(period_in: PeriodCreate, db: AsyncSession = Depends(get_db),
                        user: UserOut = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        exists = await db.execute(select(Period).where(Period.ID == period_in.ID))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Period ID already exists")

        period = Period(**period_in.model_dump())
        db.add(period)
        try:
            await db.commit()
            await db.refresh(period)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Invalid period creation")
        return period
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating period: {str(e)}")

@router.get("/", response_model=list[PeriodOut])
async def get_periods(db: AsyncSession = Depends(get_db), user: UserOut = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        result = await db.execute(select(Period))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching periods: {str(e)}")

@router.get("/active", response_model=list[PeriodOut])
async def get_active_periods_by_user_level(
    db: AsyncSession = Depends(get_db),
    user: UserOut = Depends(get_current_user)):
    try:
        now = datetime.now(timezone.utc)
        if user.level == "CAPXA":
            stmt = select(Period).where(
                Period.XaStatus == "Active",
                Period.XaActiveAt.isnot(None),
                Period.XaDeactiveAt.isnot(None),
                Period.XaActiveAt <= now,
                Period.XaDeactiveAt >= now
            )
        else:
            stmt = select(Period).where(
                Period.Status == "Active",
                Period.ActiveAt.isnot(None),
                Period.DeactiveAt.isnot(None),
                Period.ActiveAt <= now,
                Period.DeactiveAt >= now
            )
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching active periods: {str(e)}")

@router.get("/{period_id}", response_model=PeriodOut)
async def get_period(period_id: str, db: AsyncSession = Depends(get_db), user: UserOut = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        result = await db.execute(select(Period).where(Period.ID == period_id))
        period = result.scalar_one_or_none()
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")
        return period
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching period: {str(e)}")

@router.put("/{period_id}", response_model=PeriodOut)
async def update_period(period_id: str, period_in: PeriodUpdate, db: AsyncSession = Depends(get_db), user: UserOut = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        result = await db.execute(select(Period).where(Period.ID == period_id))
        period = result.scalar_one_or_none()
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")

        update_data = period_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(period, key, value)
        try:
            await db.commit()
            await db.refresh(period)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Invalid data update")

        return period
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating period: {str(e)}") 

@router.delete("/{period_id}")
async def delete_period(period_id: str, db: AsyncSession = Depends(get_db), user: UserOut = Depends(get_current_user)):
    try:
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        stmt = select(Period).options(selectinload(Period.reports)).where(Period.ID == period_id)
        result = await db.execute(stmt)
        period = result.scalar_one_or_none()
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")

        if period.reports:
            raise HTTPException(status_code=400, detail="Cannot delete period with attached reports")

        await db.delete(period)
        await db.commit()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting period: {str(e)}")

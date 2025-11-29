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


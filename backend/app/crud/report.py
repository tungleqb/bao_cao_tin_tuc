# backend/app/crud/report.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException
from ..models.report import Report
from ..models.period import Period
from ..schemas.report import ReportCreate, ReportUpdate
from sqlalchemy import func
from ..models.report import Report
from ..models.user import User  # đầu file

async def create_report(db: AsyncSession, report_in: ReportCreate):
    # Check if Report ID already exists
    try:
        result = await db.execute(select(Report).where(Report.ID == report_in.ID))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Report ID already exists")

        # Check if PeriodID exists
        period_check = await db.execute(select(Period).where(Period.ID == report_in.PeriodID))
        if not period_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Period ID does not exist")

        # ✅ Check if user is locked
        user_check = await db.execute(select(User).where(User.id == report_in.SendID))
        user = user_check.scalar_one_or_none()
        if not user or user.is_locked:
            raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa, không thể gửi báo cáo.")
        
        report = Report(**report_in.model_dump())
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report
    except Exception as e:  
        print(f"❌ Error creating report: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_reports(db: AsyncSession):
    try:
        result = await db.execute(select(Report))
        return result.scalars().all()
    except Exception as e:  
        print(f"❌ Error fetching reports: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_report(db: AsyncSession, report_id: str):
    try:
        result = await db.execute(select(Report).where(Report.ID == report_id))
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"❌ Error fetching report with ID {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def update_report(db: AsyncSession, report_id: str, report_in: ReportUpdate):
    try:
        stmt = update(Report).where(Report.ID == report_id).values(**report_in.model_dump(exclude_unset=True))
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error updating report with ID {report_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_report(db: AsyncSession, report_id: str):
    try:
        stmt = delete(Report).where(Report.ID == report_id)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        print(f"❌ Error deleting report with ID {report_id}: {e}")
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
        print(f"❌ Error updating period status with ID {period_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_report_by_sender_and_period(db: AsyncSession, sender: str, period_id: str):
    try:
        result = await db.execute(
            select(Report)
            .where(Report.Sender == sender, Report.PeriodID == period_id)
            .order_by(Report.SentAt.desc())
        )
        return result.scalars().first()
    except Exception as e:  
        print(f"❌ Error fetching report by sender and period: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_all_reports_by_sender_and_period(db: AsyncSession, sender: str, period_id: str):
    try:
        result = await db.execute(
            select(Report).where(
                Report.Sender == sender,
                Report.PeriodID == period_id
            )
        )
        return result.scalars().all()
    except Exception as e:
        print(f"❌ Error fetching all reports by sender and period: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Lấy báo cáo cuối cùng mỗi tài khoản trong kỳ
async def get_latest_reports_by_period(db: AsyncSession, period_id: str):
    try:
        subq = (
            select(
                Report.Sender,
                func.max(Report.SentAt).label("LatestTime")
            )
            .where(Report.PeriodID == period_id)
            .group_by(Report.Sender)
            .subquery()
        )

        q = (
            select(Report)
            .join(subq, (Report.Sender == subq.c.Sender) & (Report.SentAt == subq.c.LatestTime))
            .where(Report.PeriodID == period_id)
        )

        result = await db.execute(q)
        return result.scalars().all()
    except Exception as e:  
        print(f"❌ Error fetching latest reports by period: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

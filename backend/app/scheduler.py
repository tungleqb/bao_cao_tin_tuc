from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import asyncio
import logging

from .database import async_session_maker as async_session
from .crud.period import get_all_periods, update_period_status
from .crud.period_create import create_period_if_needed

logger = logging.getLogger("scheduler")
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
logger.addHandler(handler)

scheduler = AsyncIOScheduler()

# ✅ Các hàm job tạo session riêng
async def activate_status(period_id: str):
    async with async_session() as db:
        logger.info(f"[CAPPHONG] Activating Status for Period: {period_id}")
        await update_period_status(db=db, period_id=period_id, status="Active")

async def deactivate_status(period_id: str):
    async with async_session() as db:
        logger.info(f"[CAPPHONG] Deactivating Status for Period: {period_id}")
        await update_period_status(db=db, period_id=period_id, status="INACTIVE")

async def activate_xastatus(period_id: str):
    async with async_session() as db:
        logger.info(f"[CAPXA] Activating XaStatus for Period: {period_id}")
        await update_period_status(db=db, period_id=period_id, xa_status="Active")

async def deactivate_xastatus(period_id: str):
    async with async_session() as db:
        logger.info(f"[CAPXA] Deactivating XaStatus for Period: {period_id}")
        await update_period_status(db=db, period_id=period_id, xa_status="INACTIVE")

def job_exists(job_id: str):
    return scheduler.get_job(job_id) is not None

async def schedule_existing_periods():
    logger.info("Bắt đầu schedule_existing_periods")
    try:
        async with async_session() as db:
            now = datetime.now(timezone.utc)

            logger.info("⏳ Gọi create_period_if_needed PHONG")
            await create_period_if_needed(db=db, cap="CAPPHONG", now=now)

            logger.info("⏳ Gọi create_period_if_needed XA")
            await create_period_if_needed(db=db, cap="CAPXA", now=now)

            logger.info("⏳ Gọi get_all_periods")
            periods = await get_all_periods(db)

            logger.info(f"✅ Số lượng periods: {len(periods)}")
            logger.info(f">>> Dữ liệu periods: {periods}")
            for p in periods:
                logger.info(f"⛳ Period ID: {getattr(p, 'ID', p)}")  # tránh lỗi crash nếu không phải object
                logger.info(f"📅 Scheduling activate-status-{p.ID} at {p.ActiveAt}")
                # Status jobs (CAPPHONG)
                if p.ActiveAt and p.ActiveAt > now:
                    job_id = f"activate-status-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            activate_status,
                            trigger=DateTrigger(run_date=p.ActiveAt),
                            args=[p.ID],
                            id=job_id
                        )
                if p.Status != "INACTIVE" and p.DeactiveAt and p.DeactiveAt < now:
                    job_id = f"deactivate-status-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            deactivate_status,
                            trigger=DateTrigger(run_date=now),
                            args=[p.ID],
                            id=job_id
                        )
                if p.DeactiveAt and p.DeactiveAt > now:
                    job_id = f"deactivate-status-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            deactivate_status,
                            trigger=DateTrigger(run_date=p.DeactiveAt),
                            args=[p.ID],
                            id=job_id
                        )

                # XaStatus jobs (CAPXA)
                if p.XaActiveAt and p.XaActiveAt > now:
                    job_id = f"activate-xastatus-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            activate_xastatus,
                            trigger=DateTrigger(run_date=p.XaActiveAt),
                            args=[p.ID],
                            id=job_id
                        )
                if p.XaStatus != "INACTIVE" and p.XaDeactiveAt and p.XaDeactiveAt < now:
                    job_id = f"deactivate-xastatus-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            deactivate_xastatus,
                            trigger=DateTrigger(run_date=now),
                            args=[p.ID],
                            id=job_id
                        )
                if p.XaDeactiveAt and p.XaDeactiveAt > now:
                    job_id = f"deactivate-xastatus-{p.ID}"
                    if not job_exists(job_id):
                        scheduler.add_job(
                            deactivate_xastatus,
                            trigger=DateTrigger(run_date=p.XaDeactiveAt),
                            args=[p.ID],
                            id=job_id
                        )
        logger.info("✅ schedule_existing_periods SUCCESS")
    except Exception as e:
        logger.info(f"❌ schedule_existing_periods FAILED: {e}")
def start_scheduler():
    scheduler.start()

    loop = asyncio.get_event_loop()
    loop.create_task(schedule_existing_periods())

    def schedule_again():
        loop.call_soon_threadsafe(lambda: asyncio.create_task(schedule_existing_periods()))

    scheduler.add_job(
        schedule_again,
        trigger=IntervalTrigger(seconds=30),
        id="period-rescheduler",
        replace_existing=True
    )

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from ..models.period import Period
from ..models.report_type import ReportType
from ..utils.period_utils import calculate_datetime
from ..utils.period_utils import generate_all_datetimes

#from ..models.report import Report
from pathlib import Path
import os

BASE_REPORT_FOLDER = "../uploaded_reports"

async def get_valid_report_types(db: AsyncSession, cap: str, now: datetime):
    try:
        result = await db.execute(select(ReportType))
        report_types = result.scalars().all()
        valid = []
        for r in report_types:
            active_at = calculate_datetime(now,
                                        r.ActiveOffset if cap == "CAPPHONG" else r.XaActiveOffset,
                                        r.ActiveOn if cap == "CAPPHONG" else r.XaActiveOn,
                                        r.ActiveAt if cap == "CAPPHONG" else r.XaActiveAt,
                                        r.Period_ID)
            deactive_at = calculate_datetime(now,
                                            r.DeactiveOffset if cap == "CAPPHONG" else r.XaDeactiveOffset,
                                            r.DeactiveOn if cap == "CAPPHONG" else r.XaDeactiveOn,
                                            r.DeactiveAt if cap == "CAPPHONG" else r.XaDeactiveAt,
                                            r.Period_ID)
            if active_at <= now <= deactive_at:
                valid.append((r, active_at, deactive_at))
        return valid
    except Exception as e:
        print(f"❌ Lỗi khi lấy ReportType (cap={cap}): {e}")
        return None

async def create_period_if_needed(db: AsyncSession, cap: str, now: datetime):
    try:
        report_type_with_times = await get_valid_report_types(db, cap, now)
        new_periods = []
        for rt, _, _ in report_type_with_times:
            # Dựng toàn bộ mốc thời gian
            datetimes = generate_all_datetimes(now, rt)

            phong_valid = datetimes["ActiveAt"] <= now <= datetimes["DeactiveAt"]
            xa_valid = datetimes["XaActiveAt"] and datetimes["XaActiveAt"] <= now <= datetimes["XaDeactiveAt"]

            if not (phong_valid or xa_valid):
                continue  # Không hợp lệ ở cả 2 cấp → bỏ

            new_id = f"{rt.ID}_{datetimes['ActiveAt'].strftime('%Y%m%d%H%M%S')}"
            exists = await db.execute(select(Period).where(Period.ID == new_id))
            if exists.scalar_one_or_none():
                continue

            folder_path = os.path.join(BASE_REPORT_FOLDER, new_id)
            os.makedirs(folder_path, exist_ok=True)
            pr_name = f"{rt.Name}"
            if rt.Period_ID == "DAILY":
                pr_name = f"{rt.Name} - {datetimes['ActiveAt'].strftime('%d/%m/%Y')}"
            elif rt.Period_ID == "WEEKLY":
                pr_name = f"{rt.Name} từ {datetimes['FromAt'].strftime('%d/%m/%Y')} đến {datetimes['ToAt'].strftime('%d/%m/%Y')}"
            elif rt.Period_ID == "MONTHLY":
                pr_name = f"{rt.Name} - {datetimes['ActiveAt'].strftime('%m/%Y')}"
            period = Period(
                ID=new_id,
                Name=pr_name,
                TYPE=rt.ID,
                ActiveAt=datetimes["ActiveAt"],
                DeactiveAt=datetimes["DeactiveAt"],
                StartAt=datetimes["StartAt"],
                EndAt=datetimes["EndAt"],
                FromAt=datetimes["FromAt"],
                ToAt=datetimes["ToAt"],
                XaActiveAt=datetimes["XaActiveAt"],
                XaDeactiveAt=datetimes["XaDeactiveAt"],
                XaStartAt=datetimes["XaStartAt"],
                XaEndAt=datetimes["XaEndAt"],
                XaFromAt=datetimes["XaFromAt"],
                XaToAt=datetimes["XaToAt"],
                Status="Active" if phong_valid else "Deactive",
                XaStatus="Active" if xa_valid else "Deactive",
                FolderPath=folder_path,
                Killer="Auto"
            )
            db.add(period)
            new_periods.append(period)

    except Exception as e:
        print(f"❌ Lỗi khi tạo Period (cap={cap}): {e}")
        return None
    if new_periods:
        try:
            await db.commit()
            for p in new_periods:
                await db.refresh(p)
        except Exception as e:
            await db.rollback()
            print(f"❌ Lỗi khi commit tạo Period (cap={cap}): {e}")

    return new_periods

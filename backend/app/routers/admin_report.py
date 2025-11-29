# backend/app/routers/report.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..crud import report as crud_report
from ..crud import audit_log as crud_audit_log
from ..models.period import Period
from ..models.report_type import ReportType
from ..models.report import Report
from ..schemas.report import ReportCreate, ReportOut, ReportStatus
from ..schemas.audit_log import AuditLogCreate
from ..dependencies.auth import get_current_admin
from ..database import get_db
import os
import hashlib
from datetime import datetime, timezone
from ..models.user import User

from fastapi.responses import FileResponse
import zipfile
import tempfile
import uuid

router = APIRouter(prefix="/admin/report", tags=["Report"])

@router.get("/{period_id}", response_model=list[ReportOut])
async def get_reports_by_period(
    period_id: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        from ..crud import report as crud_report
        reports = await crud_report.get_latest_reports_by_period(db, period_id)
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")
   
@router.get("/download/{period_id}")
async def download_period_folder(
    period_id: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)  # ✅ Chỉ cho admin
    ):
    #try:
    result = await db.execute(select(Period).where(Period.ID == period_id))
    period = result.scalar_one_or_none()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")

    folder_path = period.FolderPath
    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="Folder not found")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname=relative_path)

    zip_filename = f"{period_id}.zip"
    return FileResponse(tmp.name, filename=zip_filename, media_type="application/zip")
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Failed to download folder: {str(e)}")

@router.get("/download/{period_id}/sender/{sender}")
async def download_report_by_sender(
    period_id: str,
    sender: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        report = await crud_report.get_report_by_sender_and_period(db, sender, period_id)
        if not report:
            raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo phù hợp.")

        if not os.path.exists(report.FilePath):
            raise HTTPException(status_code=404, detail="File báo cáo không còn tồn tại.")

        return FileResponse(
            path=report.FilePath,
            filename=report.FileName,  # Tên file server để frontend tải đúng tên
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tải báo cáo: {str(e)}")

@router.get("/missing/{period_id}")
async def get_missing_senders_in_period(
    period_id: str,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        # Lấy danh sách user không phải admin
        user_result = await db.execute(
            select(User).where(User.is_admin == False, User.is_locked == False)
        )
        users = user_result.scalars().all()
        user_dict = {u.id: u for u in users}

        # Lấy danh sách ID đã gửi báo cáo kỳ này
        report_result = await db.execute(
            select(Report.SendID).where(Report.PeriodID == period_id)
        )
        sent_ids = set(row[0] for row in report_result.all())

        # Lọc ra user chưa gửi
        missing_users = [
            {
                "id": u.id,
                "username": u.username,
                "name": u.name
            }
            for uid, u in user_dict.items()
            if uid not in sent_ids
        ]
        return missing_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách thiếu báo cáo: {str(e)}")





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
from ..dependencies.auth import get_current_user
from ..database import get_db
import os
import hashlib
from datetime import datetime, timezone
 
from fastapi.responses import FileResponse
import zipfile
import tempfile
import uuid

router = APIRouter(prefix="/report", tags=["Report"])

@router.post("/upload", response_model=ReportOut)
async def upload_report(
    file: UploadFile = File(...),
    #report_type_id: str = Form(...),
    period_id: str = Form(...),
    comment: str = Form(""),
    has_event: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)):
    report = None
    try:
        #print("⏳ Bắt đầu upload")
        now = datetime.now(timezone.utc)

        # Kiểm tra kỳ báo cáo
        period_result = await db.execute(select(Period).where(Period.ID == period_id))
        period = period_result.scalar_one_or_none()
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")

        #print(f"✅ Period: {period.ID}")
        # Kiểm tra loại báo cáo
        report_type_result = await db.execute(select(ReportType).where(ReportType.ID == period.TYPE))
        report_type = report_type_result.scalar_one_or_none()
        if not report_type:
            raise HTTPException(status_code=404, detail="ReportType not found")
        report_type_id = report_type.ID
        #print(f"✅ ReportType: {report_type.ID}")
        # Kiểm tra trạng thái theo cấp tài khoản
        if user.level == "CAPXA":
            if period.XaStatus != "Active":
                raise HTTPException(status_code=400, detail="This reporting period is not active for your level.")
        else:
            if period.Status != "Active":
                raise HTTPException(status_code=400, detail="This reporting period is not active.")

        #print(f"✅ ReportType: {report_type.MaxSize[:-2]}")
        # Đọc và kiểm tra file
        content = await file.read()
        if len(content) > float(report_type.MaxSize[:-2]) * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File size exceeds {report_type.MaxSize} limit")

        #print(f"✅ ReportType: {report_type.ID}")
        ext_list = (report_type.DocExtList or "").lower().split()
        ext_list = [e.strip().lstrip(".") for e in ext_list if e.strip()]
        file_ext = file.filename.lower().rsplit(".", 1)[-1]
        if file_ext not in ext_list:
            raise HTTPException(status_code=400, detail=f"Invalid file extension '.{file_ext}'. Allowed: {', '.join(ext_list)}")
        
        #print(f"✅ File check OK: {file.filename}")

        checksum = hashlib.blake2b(content).hexdigest()
        #print(f"✅ Checksum: {checksum}")

        # Tạo đường dẫn lưu file
        folder_path = period.FolderPath
        full_folder_path = folder_path
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{user.username}_{period.ID}_{timestamp_str}.{file_ext}"    
        #new_filename = f"{user.username}_{period.ID}.{file_ext}"
        if period.TYPE[:5] == "DAILY":
            subfolder = "has_event" if has_event else "no_event"
            full_folder_path = os.path.join(folder_path, subfolder)

        os.makedirs(full_folder_path, exist_ok=True)

        save_path = os.path.join(full_folder_path, new_filename)
        with open(save_path, "wb") as f:
            f.write(content)

        # Tính độ trễ
        if now < period.StartAt:
            late_seconds = int((now - period.StartAt).total_seconds())
        elif now > period.EndAt:
            late_seconds = int((now - period.EndAt).total_seconds())
        else:
            late_seconds = 0

        # Sinh ID tránh trùng
        report_id = f"{user.username}_{period_id}_{uuid.uuid4().hex[:8]}"

        old_reports = await crud_report.get_all_reports_by_sender_and_period(db, user.username, period_id)

        report_in = ReportCreate(
            ID=report_id,
            Sender=user.username,
            SendID=user.id,
            PeriodID=period_id,
            ReportTypeID=report_type_id,
            ReportPeriodName=period.Name,
            Blake3sum=checksum,
            FilePath=save_path,
            FileName= new_filename,
            OriFileName=file.filename,
            FileSize=len(content),
            SentAt=now,
            Comment=comment,
            HasEvent=has_event,
            LateSeconds=late_seconds,
        )

        # Ghi báo cáo
        report = await crud_report.create_report(db, report_in)
        #print("📦 Gọi create_report")
        # Sau khi ghi báo cáo mới thành công
        for old in old_reports:
            if old.FilePath and os.path.exists(old.FilePath):
                try:
                    os.remove(old.FilePath)
                    print(f"🧹 Đã xoá file cũ: {old.FilePath}")
                except Exception as e:
                    print(f"⚠️ Không thể xoá file {old.FilePath}: {e}")

        try:
            await crud_audit_log.create_audit_log(db, AuditLogCreate(
                user_id=user.id,
                action="UPLOAD_REPORT",
                model="Report",
                model_id=report.ID,
                details=f"Uploaded report {report.ID}",
                timestamp=now.replace(tzinfo=None)
            ))
        except Exception as e:
            print(f"⚠️ Audit log failed: {e}")
    except Exception as e:
        print(f"❌ Lỗi khi upload báo cáo: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload report")
    return report

@router.get("/reports", response_model=list[ReportOut])
async def get_my_reports(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    try:
        all_reports = await crud_report.get_reports(db)
        return [r for r in all_reports if r.SendID == user.id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")


@router.get("/{period_id}", response_model=ReportStatus)
async def get_user_report_for_period(
    period_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)):
    try:
        result = await db.execute(
            select(Report)
            .where(Report.PeriodID == period_id, Report.SendID == user.id)
            .order_by(Report.SentAt.desc())
        )
        report = result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    if not report:
        return ReportStatus(Status="not_sent")

    return ReportStatus(
        Status="sent",
        Blake3sum=report.Blake3sum,
        SentAt=report.SentAt,
        LateSeconds=report.LateSeconds,
        HasEvent=report.HasEvent,
        OriFileName=report.OriFileName,
        ID=report.ID
    )

@router.get("/download/me/{period_id}")
async def download_my_report(
    period_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        # Tìm báo cáo mới nhất của người dùng trong kỳ
        report = await crud_report.get_report_by_sender_and_period(db, user.username, period_id)
        if not report:
            raise HTTPException(status_code=404, detail="Bạn chưa gửi báo cáo trong kỳ này.")

        if not os.path.exists(report.FilePath):
            raise HTTPException(status_code=404, detail="File báo cáo không còn tồn tại trên hệ thống.")
        print(report.FilePath)
        return FileResponse(
            path=report.FilePath,
            filename=report.OriFileName,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Lỗi khi tải file cá nhân: {e}")
        raise HTTPException(status_code=500, detail="Không thể tải file báo cáo.")




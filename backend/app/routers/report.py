
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models.report import Report
from ..models.loai_baocao import LoaiBaoCao
from ..schemas.report import ReportOut
from ..dependencies.auth import get_current_user
from datetime import datetime
import os
from pathlib import Path
from unidecode import unidecode

router = APIRouter()

@router.post("/upload", response_model=ReportOut)
async def upload_report(
    file: UploadFile = File(...),
    loai_baocao_id: int = Form(...),
    has_event: bool = Form(True),
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    loai = await db.get(LoaiBaoCao, loai_baocao_id)
    if not loai:
        raise HTTPException(status_code=404, detail="Loại báo cáo không tồn tại")

    now = datetime.now()
    is_late = now > loai.han_gui
    late_seconds = int((now - loai.han_gui).total_seconds()) if is_late else 0

    ext = file.filename.split(".")[-1]
    filename_raw = f"{user.ten_chi_nhanh}_{loai.ten_loai}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.{ext}"
    filename = unidecode(filename_raw).replace(" ", "_")
    base_dir = Path("static/reports") / unidecode(loai.ten_loai).replace(" ", "_") / now.strftime("%Y-%m-%d")
    if loai.ten_loai.lower() == "báo cáo ngày":
        base_dir = base_dir / ("co_su_kien" if has_event else "khong_su_kien")
    os.makedirs(base_dir, exist_ok=True)

    path = base_dir / filename
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    new_report = Report(
        loai_baocao_id=loai_baocao_id,
        user_id=user.id,
        filename=str(filename),
        filesize=len(content),
        has_event=has_event,
        is_late=is_late,
        late_seconds=late_seconds
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    return new_report

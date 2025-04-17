from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..database import get_db
from ..models.yeu_cau_baocao import YeuCauBaoCao
from ..models.user import User
from ..schemas.yeu_cau import YeuCauBaoCaoCreate, YeuCauBaoCaoOut
from ..dependencies.auth import get_current_admin

router = APIRouter()

@router.post("/", response_model=YeuCauBaoCaoOut)
async def create_request(data: YeuCauBaoCaoCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    users = await db.execute(select(User).where(User.id.in_(data.user_ids)))
    user_list = users.scalars().all()
    if not user_list:
        raise HTTPException(status_code=404, detail="Không tìm thấy chi nhánh")

    req = YeuCauBaoCao(
        loai_baocao_id=data.loai_baocao_id,
        dinh_ky_value=data.dinh_ky_value,
        dinh_ky_unit=data.dinh_ky_unit,
        is_active=data.is_active,
        users=user_list
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return YeuCauBaoCaoOut(
        id=req.id,
        loai_baocao_id=req.loai_baocao_id,
        dinh_ky_value=req.dinh_ky_value,
        dinh_ky_unit=req.dinh_ky_unit,
        is_active=req.is_active,
        user_ids=[u.id for u in req.users]
    )

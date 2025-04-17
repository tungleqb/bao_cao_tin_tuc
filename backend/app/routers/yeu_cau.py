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
from ..crud.audit_log import log_action

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
    await log_action(db, admin.id, "update", "YeuCauBaoCao", req.id, "Cập nhật yêu cầu báo cáo")
    await log_action(db, admin.id, "create", "YeuCauBaoCao", req.id, f"Tạo yêu cầu báo cáo tới {len(user_list)} chi nhánh")
    return YeuCauBaoCaoOut(
        id=req.id,
        loai_baocao_id=req.loai_baocao_id,
        dinh_ky_value=req.dinh_ky_value,
        dinh_ky_unit=req.dinh_ky_unit,
        is_active=req.is_active,
        user_ids=[u.id for u in req.users]
    )

@router.get("/", response_model=list[YeuCauBaoCaoOut])
async def get_requests(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(
        select(YeuCauBaoCao).options(selectinload(YeuCauBaoCao.users))
    )
    requests = result.scalars().all()
    return [
        YeuCauBaoCaoOut(
            id=r.id,
            loai_baocao_id=r.loai_baocao_id,
            dinh_ky_value=r.dinh_ky_value,
            dinh_ky_unit=r.dinh_ky_unit,
            is_active=r.is_active,
            user_ids=[u.id for u in r.users]
        ) for r in requests
    ]

@router.put("/{id}", response_model=YeuCauBaoCaoOut)
async def update_request(id: int, data: YeuCauBaoCaoCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(YeuCauBaoCao).where(YeuCauBaoCao.id == id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Không tìm thấy yêu cầu")

    user_result = await db.execute(select(User).where(User.id.in_(data.user_ids)))
    req.users = user_result.scalars().all()
    req.loai_baocao_id = data.loai_baocao_id
    req.dinh_ky_value = data.dinh_ky_value
    req.dinh_ky_unit = data.dinh_ky_unit
    req.is_active = data.is_active

    await db.commit()
    await db.refresh(req)
    await log_action(db, admin.id, "create", "YeuCauBaoCao", req.id, f"Tạo yêu cầu báo cáo tới {len(user_list)} chi nhánh")

    return YeuCauBaoCaoOut(
        id=req.id,
        loai_baocao_id=req.loai_baocao_id,
        dinh_ky_value=req.dinh_ky_value,
        dinh_ky_unit=req.dinh_ky_unit,
        is_active=req.is_active,
        user_ids=[u.id for u in req.users]
    )

@router.delete("/{id}")
async def delete_request(id: int, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(YeuCauBaoCao).where(YeuCauBaoCao.id == id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Không tìm thấy yêu cầu")

    await db.delete(req)
    await db.commit()
    await log_action(db, admin.id, "delete", "YeuCauBaoCao", req.id, "Xoá yêu cầu báo cáo")
    return {"msg": "Đã xoá yêu cầu báo cáo"}

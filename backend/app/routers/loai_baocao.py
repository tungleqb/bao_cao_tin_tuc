
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.loai_baocao import LoaiBaoCaoCreate, LoaiBaoCaoOut
from ..models.loai_baocao import LoaiBaoCao
from ..dependencies.auth import get_current_admin, get_current_user
from ..database import get_db
from ..crud.audit_log import log_action

router = APIRouter()

@router.get("/", response_model=list[LoaiBaoCaoOut])
async def get_all(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(LoaiBaoCao))
    return result.scalars().all()

@router.post("/", response_model=LoaiBaoCaoOut)
async def create(item: LoaiBaoCaoCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    obj = LoaiBaoCao(**item.dict())
    db.add(obj)
    await db.commit()
    await log_action(db, admin.id, "create", "LoaiBaoCao", obj.id, f"Tạo loại báo cáo: {item.ten_loai}")
    await db.refresh(obj)
    return obj

@router.put("/{id}", response_model=LoaiBaoCaoOut)
async def update(id: int, item: LoaiBaoCaoCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(LoaiBaoCao).where(LoaiBaoCao.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    for k, v in item.dict().items():
        setattr(obj, k, v)
    await db.commit()
    await log_action(db, admin.id, "update", "LoaiBaoCao", id, f"Cập nhật loại báo cáo: {item.ten_loai}")
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(LoaiBaoCao).where(LoaiBaoCao.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    await db.delete(obj)
    await db.commit()
    await log_action(db, admin.id, "delete", "LoaiBaoCao", id, f"Xoá loại báo cáo: {obj.ten_loai}")
    return {"msg": "Đã xoá"}

@router.get("/public", response_model=list[LoaiBaoCaoOut], tags=["Loại báo cáo công khai"])
async def get_all_public(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(LoaiBaoCao))
    return result.scalars().all()
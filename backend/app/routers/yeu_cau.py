from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse
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
        dinh_ky=data.dinh_ky,
        users=user_list
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return YeuCauBaoCaoOut.from_orm_with_users(req)

@router.get("/")
async def get_all_requests(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(
        select(YeuCauBaoCao).options(selectinload(YeuCauBaoCao.users))
    )
    all_requests = result.scalars().all()

    data = []
    for req in all_requests:
        data.append({
            "id": req.id,
            "loai_baocao_id": req.loai_baocao_id,
            "dinh_ky": req.dinh_ky,
            "user_ids": [u.id for u in req.users]
        })

    return JSONResponse(content=data)
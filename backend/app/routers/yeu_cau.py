
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..database import get_db
from ..models.yeu_cau_baocao import YeuCauBaoCao
from ..models.user import User
from ..schemas.yeu_cau import YeuCauBaoCaoCreate, YeuCauBaoCaoOut, ActiveUpdate
from ..dependencies.auth import get_current_admin, get_current_user
from ..crud.audit_log import log_action

router = APIRouter()

# (các API cũ)...

@router.get("/my", response_model=list[YeuCauBaoCaoOut])
async def get_my_requests(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(YeuCauBaoCao)
        .options(selectinload(YeuCauBaoCao.users))
        .where(YeuCauBaoCao.is_active == True)
    )
    all_requests = result.scalars().all()
    filtered = [r for r in all_requests if any(u.id == user.id for u in r.users)]
    return [
        YeuCauBaoCaoOut(
            id=r.id,
            loai_baocao_id=r.loai_baocao_id,
            dinh_ky_value=r.dinh_ky_value,
            dinh_ky_unit=r.dinh_ky_unit,
            is_active=r.is_active,
            user_ids=[u.id for u in r.users]
        ) for r in filtered
    ]

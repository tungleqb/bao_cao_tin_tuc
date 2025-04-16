from pydantic import BaseModel
from typing import List
from pydantic import Field

class YeuCauBaoCaoCreate(BaseModel):
    loai_baocao_id: int
    user_ids: List[int]
    dinh_ky: int = 0

class YeuCauBaoCaoOut(BaseModel):
    id: int
    loai_baocao_id: int
    dinh_ky: int
    user_ids: List[int] = Field(...)

    @staticmethod
    def from_orm_with_users(obj):
        return YeuCauBaoCaoOut(
            id=obj.id,
            loai_baocao_id=obj.loai_baocao_id,
            dinh_ky=obj.dinh_ky,
            user_ids=[user.id for user in obj.users],
        )

    class Config:
        orm_mode = True

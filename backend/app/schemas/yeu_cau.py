from pydantic import BaseModel
from typing import List

class YeuCauBaoCaoCreate(BaseModel):
    loai_baocao_id: int
    user_ids: List[int]
    dinh_ky: int = 0

class YeuCauBaoCaoOut(YeuCauBaoCaoCreate):
    id: int

    class Config:
        from_attributes = True

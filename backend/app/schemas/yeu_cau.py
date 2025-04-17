from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class ActiveUpdate(BaseModel):
    is_active: bool

class DinhKyEnum(str, Enum):
    hour = "hour"
    day = "day"
    month = "month"

class YeuCauBaoCaoCreate(BaseModel):
    loai_baocao_id: int
    user_ids: List[int]
    dinh_ky_value: int = 0
    dinh_ky_unit: DinhKyEnum = DinhKyEnum.day
    is_active: bool = True

class YeuCauBaoCaoOut(BaseModel):
    id: int
    loai_baocao_id: int
    dinh_ky_value: int
    dinh_ky_unit: DinhKyEnum
    is_active: bool
    user_ids: List[int] = Field(...)

    class Config:
        from_attributes = True

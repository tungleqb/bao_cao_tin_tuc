
from pydantic import BaseModel
from datetime import datetime

class LoaiBaoCaoBase(BaseModel):
    ten_loai: str
    thoi_gian_bat_dau: datetime
    han_gui: datetime
    dinh_ky: int = 0

class LoaiBaoCaoCreate(LoaiBaoCaoBase):
    pass

class LoaiBaoCaoOut(LoaiBaoCaoBase):
    id: int

    class Config:
        from_attributes = True

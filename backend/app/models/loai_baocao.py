
from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class LoaiBaoCao(Base):
    __tablename__ = "loai_baocao"

    id = Column(Integer, primary_key=True, index=True)
    ten_loai = Column(String, nullable=False)
    from sqlalchemy import DateTime
    thoi_gian_bat_dau = Column(DateTime(timezone=True), nullable=False)
    han_gui = Column(DateTime(timezone=True), nullable=False)
    dinh_ky = Column(Integer, default=0)  # đơn vị giờ/ngày/tuần...

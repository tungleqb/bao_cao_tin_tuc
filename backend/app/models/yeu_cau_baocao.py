from sqlalchemy import Column, Integer, ForeignKey, Table, Boolean, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

yeu_cau_user_table = Table(
    "yeu_cau_user", Base.metadata,
    Column("yeu_cau_id", ForeignKey("yeu_cau_baocao.id")),
    Column("user_id", ForeignKey("users.id")),
)

class DinhKyEnum(str, enum.Enum):
    hour = "hour"
    day = "day"
    month = "month"

class YeuCauBaoCao(Base):
    __tablename__ = "yeu_cau_baocao"

    id = Column(Integer, primary_key=True, index=True)
    loai_baocao_id = Column(Integer, ForeignKey("loai_baocao.id"))
    dinh_ky_value = Column(Integer, default=0)
    dinh_ky_unit = Column(Enum(DinhKyEnum), default=DinhKyEnum.day)
    is_active = Column(Boolean, default=True)

    users = relationship("User", secondary=yeu_cau_user_table)

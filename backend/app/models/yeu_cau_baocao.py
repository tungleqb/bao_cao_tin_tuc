from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

yeu_cau_user_table = Table(
    "yeu_cau_user", Base.metadata,
    Column("yeu_cau_id", ForeignKey("yeu_cau_baocao.id")),
    Column("user_id", ForeignKey("users.id")),
)

class YeuCauBaoCao(Base):
    __tablename__ = "yeu_cau_baocao"

    id = Column(Integer, primary_key=True, index=True)
    loai_baocao_id = Column(Integer, ForeignKey("loai_baocao.id"))
    dinh_ky = Column(Integer, default=0)

    users = relationship("User", secondary=yeu_cau_user_table)

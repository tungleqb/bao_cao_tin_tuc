from datetime import datetime
from pydantic import BaseModel, field_validator
from pydantic import ConfigDict

class PeriodBase(BaseModel):
    TYPE: str
    ID: str
    Name: str

    ActiveAt: datetime
    DeactiveAt: datetime
    StartAt: datetime
    EndAt: datetime
    FromAt: datetime
    ToAt: datetime

    XaActiveAt: datetime | None = None
    XaDeactiveAt: datetime | None = None
    XaStartAt: datetime | None = None
    XaEndAt: datetime | None = None
    XaFromAt: datetime | None = None
    XaToAt: datetime | None = None

    Status: str
    XaStatus: str | None = None

    Killer: str
    FolderPath: str

    # ✅ VALIDATORS
    @field_validator("EndAt")
    def validate_end_after_start(cls, v, info):
        if v <= info.data["StartAt"]:
            raise ValueError("EndAt phải sau StartAt")
        return v

    @field_validator("ToAt")
    def validate_to_after_from(cls, v, info):
        if v <= info.data["FromAt"]:
            raise ValueError("ToAt phải sau FromAt")
        return v

    @field_validator("XaEndAt")
    def validate_xa_end_after_start(cls, v, info):
        start = info.data.get("XaStartAt")
        if v and start and v <= start:
            raise ValueError("XaEndAt phải sau XaStartAt")
        return v

    @field_validator("XaToAt")
    def validate_xa_to_after_from(cls, v, info):
        from_ = info.data.get("XaFromAt")
        if v and from_ and v <= from_:
            raise ValueError("XaToAt phải sau XaFromAt")
        return v

    @field_validator("XaStartAt")
    def validate_xa_start_after_active(cls, v, info):
        active = info.data.get("XaActiveAt")
        if v and active and v < active:
            raise ValueError("XaStartAt phải sau hoặc bằng XaActiveAt")
        return v

    @field_validator("StartAt")
    def validate_start_after_active(cls, v, info):
        active = info.data.get("ActiveAt")
        if v < active:
            raise ValueError("StartAt phải sau hoặc bằng ActiveAt")
        return v

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    Name: str | None = None
    Status: str | None = None
    XaStatus: str | None = None
    Killer: str | None = None

class PeriodOut(PeriodBase):
    model_config = ConfigDict(from_attributes=True)
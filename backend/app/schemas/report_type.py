from datetime import datetime, time
from pydantic import BaseModel
from typing import Optional, Literal
from pydantic import ConfigDict
from pydantic import BaseModel, field_validator, ValidationInfo
from ..utils.period_utils import calculate_datetime

# Định nghĩa kiểu cho Period_ID
PeriodIDType = Literal["DAILY", "WEEKLY", "MONTHLY", "NONE"]

class ReportTypeBase(BaseModel):
    Name: str
    Period_ID: PeriodIDType

    ActiveOffset: int = 0
    ActiveOn: int = 0
    ActiveAt: time

    DeactiveOffset: int = 0
    DeactiveOn: int = 0
    DeactiveAt: time

    StartOffset: int = 0
    StartOn: int = 0
    StartAt: time

    EndOffset: int = 0
    EndOn: int = 0
    EndAt: time

    FromOffset: int = 0
    FromOn: int = 0
    From: time

    ToOffset: int = 0
    ToOn: int = 0
    To: time

    XaActiveOffset: int = 0
    XaActiveOn: int = 0
    XaActiveAt: time

    XaDeactiveOffset: int = 0
    XaDeactiveOn: int = 0
    XaDeactiveAt: time

    XaStartOffset: int = 0
    XaStartOn: int = 0
    XaStartAt: time

    XaEndOffset: int = 0
    XaEndOn: int = 0
    XaEndAt: time

    XaFromOffset: int = 0
    XaFromOn: int = 0
    XaFromAt: time

    XaToOffset: int = 0
    XaToOn: int = 0
    XaToAt: time

    DocExtList: Optional[str] = ".doc .docx .pdf .bm2 .jpg .xlsx .xls"
    MaxSize: Optional[str] = "100MB"
    #NextAt: Optional[datetime] = None

    # Validator mới
    
    @field_validator("EndAt")
    def validate_end_after_start(cls, end_at, info: ValidationInfo):
        data = info.data
        required_fields = ["Period_ID", "StartOffset", "StartOn", "StartAt", "EndOffset", "EndOn"]
        
        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ mốc thời gian")

        period_id = data["Period_ID"]

        base_date = datetime(2025, 1, 1)  # ngày cơ sở tham chiếu (bất kỳ)

        # Tính toán mốc thời gian Start
        start_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["StartOffset"],
            on=data["StartOn"],
            at=data["StartAt"],
            period_id=period_id
        )

        # Tính toán mốc thời gian End
        end_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["EndOffset"],
            on=data["EndOn"],
            at=end_at,
            period_id=period_id
        )
        print(f"Start: {start_datetime}, End: {end_datetime}")
        # Kiểm tra điều kiện
        if end_datetime <= start_datetime:
            raise ValueError("Thời điểm (EndOffset, EndOn, EndAt) phải lớn hơn (StartOffset, StartOn, StartAt)")

        return end_at
    
    @field_validator("To")
    def validate_to_after_from(cls, to_at, info: ValidationInfo):
        data = info.data
        required_fields = ["Period_ID", "FromOffset", "FromOn", "From", "ToOffset", "ToOn"]

        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ To và From")

        period_id = data["Period_ID"]
        base_date = datetime(2025, 1, 1)

        from_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["FromOffset"],
            on=data["FromOn"],
            at=data["From"],
            period_id=period_id
        )

        to_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["ToOffset"],
            on=data["ToOn"],
            at=to_at,
            period_id=period_id
        )
        print(f"From: {from_datetime}, To: {to_datetime}")
        # Kiểm tra điều kiện
        if to_datetime <= from_datetime:
            raise ValueError("Thời điểm (ToOffset, ToOn, To) phải lớn hơn (FromOffset, FromOn, From)")

        return to_at

    @field_validator("XaEndAt")
    def validate_xa_end_after_start(cls, xa_end_at, info: ValidationInfo): 
        data = info.data
        required_fields = ["Period_ID", "XaStartOffset", "XaStartOn", "XaStartAt", "XaEndOffset", "XaEndOn"]

        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ XaStartAt và XaEndAt")

        period_id = data["Period_ID"]
        base_date = datetime(2025, 1, 1)

        xa_start_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaStartOffset"],
            on=data["XaStartOn"],
            at=data["XaStartAt"],
            period_id=period_id
        )

        xa_end_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaEndOffset"],
            on=data["XaEndOn"],
            at=xa_end_at,
            period_id=period_id
        )
        print(f"XaStart: {xa_start_datetime}, XaEnd: {xa_end_datetime}")
        # Kiểm tra điều kiện
        if xa_end_datetime <= xa_start_datetime:
            raise ValueError("Thời điểm (XaEndOffset, XaEndOn, XaEndAt) phải lớn hơn (XaStartOffset, XaStartOn, XaStartAt)")

        return xa_end_at
    
    @field_validator("XaToAt")
    def validate_xa_to_after_from(cls, xa_to_at, info: ValidationInfo):
        data = info.data
        required_fields = ["Period_ID", "XaFromOffset", "XaFromOn", "XaFromAt", "XaToOffset", "XaToOn"]

        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ  XaToAt và XaFromAt")
        period_id = data["Period_ID"]
        base_date = datetime(2025, 1, 1)

        xa_from_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaFromOffset"],
            on=data["XaFromOn"],
            at=data["XaFromAt"],
            period_id=period_id
        )

        xa_to_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaToOffset"],
            on=data["XaToOn"],
            at=xa_to_at,
            period_id=period_id
        )
        print(f"XaFrom: {xa_from_datetime}, XaTo: {xa_to_datetime}")
        # Kiểm tra điều kiện
        if xa_to_datetime <= xa_from_datetime:
            raise ValueError("Thời điểm (XaToOffset, XaToOn, XaToAt) phải lớn hơn (XaFromOffset, XaFromOn, XaFromAt)")

        return xa_to_at
    
    @field_validator("DeactiveAt")
    def validate_deactive_after_active(cls, deactive_at, info: ValidationInfo):
        data = info.data
        required_fields = ["Period_ID", "ActiveOffset", "ActiveOn", "ActiveAt", "DeactiveOffset", "DeactiveOn"]

        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ DeactiveAt và ActiveAt")

        period_id = data["Period_ID"]
        base_date = datetime(2025, 1, 1)

        active_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["ActiveOffset"],
            on=data["ActiveOn"],
            at=data["ActiveAt"],
            period_id=period_id
        )

        deactive_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["DeactiveOffset"],
            on=data["DeactiveOn"],
            at=deactive_at,
            period_id=period_id
        )
        print(f"Active: {active_datetime}, Deactive: {deactive_datetime}")
        # Kiểm tra điều kiện    
        if deactive_datetime <= active_datetime:
            raise ValueError("Thời điểm (DeactiveOffset, DeactiveOn, DeactiveAt) phải lớn hơn (ActiveOffset, ActiveOn, ActiveAt)")

        return deactive_at

    @field_validator("XaDeactiveAt")
    def validate_xa_deactive_after_active(cls, xa_deactive_at, info: ValidationInfo):
        data = info.data
        required_fields = ["Period_ID", "XaActiveOffset", "XaActiveOn", "XaActiveAt", "XaDeactiveOffset", "XaDeactiveOn"]

        if not all(k in data for k in required_fields):
            raise ValueError("Thiếu thông tin để kiểm tra hợp lệ XaActiveAt và XaDeactiveAt")

        period_id = data["Period_ID"]
        base_date = datetime(2025, 1, 1)

        xa_active_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaActiveOffset"],
            on=data["XaActiveOn"],
            at=data["XaActiveAt"],
            period_id=period_id
        )

        xa_deactive_datetime = calculate_datetime(
            base_date=base_date,
            offset=data["XaDeactiveOffset"],
            on=data["XaDeactiveOn"],
            at=xa_deactive_at,
            period_id=period_id
        )

        print(f"XaActive: {xa_active_datetime}, XaDeactive: {xa_deactive_datetime}")
        # Kiểm tra điều kiện
        if xa_deactive_datetime <= xa_active_datetime:
            raise ValueError("Thời điểm (XaDeactiveOffset, XaDeactiveOn, XaDeactiveAt) phải lớn hơn (XaActiveOffset, XaActiveOn, XaActiveAt)")

        return xa_deactive_at

    
class ReportTypeCreate(ReportTypeBase):
    #ID: str
    #DateCreated: datetime
    pass

class ReportTypeUpdate(ReportTypeBase):
    #ID: str
    #DateCreated: datetime
    #NextAt: Optional[datetime] = None
    pass

class ReportTypeOut(ReportTypeCreate):
    ID: str
    DateCreated: datetime
    NextAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

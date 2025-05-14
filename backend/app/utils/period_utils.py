
from datetime import datetime, timedelta, time, date, timezone

def validate_offset_on_at(offset: int, on: int, at: time, period_id: str):
    if period_id == "WEEKLY":
        if not (0 <= on <= 6):
            raise ValueError("Với WEEKLY, giá trị 'On' phải nằm trong khoảng 0-6 (0 là Thứ 2).")
    elif period_id == "MONTHLY":
        if not (1 <= on <= 31):
            raise ValueError("Với MONTHLY, giá trị 'On' phải nằm trong khoảng 1-31.")
    elif period_id == "DAILY":
        if on != 0:
            raise ValueError("Với DAILY, giá trị 'On' phải là 0.")
    elif period_id == "NONE":
        if offset != 0 or on != 0:
            raise ValueError("Với NONE, 'Offset' và 'On' phải là 0.")

def calculate_datetime(base_date: datetime, offset: int, on, at: time, period_id: str) -> datetime:
    try:
        if period_id == "NONE":
            if not isinstance(on, date):
                raise ValueError("With Period_ID = 'NONE', `on` must be a `datetime.date` object")
            return datetime.combine(on, at)
        if period_id == "WEEKLY":
            # Tìm thứ Hai gần nhất về trước
            anchor = base_date - timedelta(days=base_date.weekday())
            shifted = anchor + timedelta(weeks=offset)
            if on:
                shifted += timedelta(days=on - 1)
        elif period_id == "MONTHLY":
            # Về ngày đầu tháng
            anchor = base_date.replace(day=1)
            month = anchor.month + offset
            year = anchor.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            shifted = anchor.replace(year=year, month=month)
            if on:
                shifted = shifted.replace(day=on)
        else:  # DAILY
            shifted = base_date + timedelta(days=offset)
            if on:
                shifted += timedelta(days=on)
        result = datetime.combine(shifted.date(), at)
        return result.replace(tzinfo=timezone.utc)
    except Exception as e:
        print(f"❌ Lỗi khi tính toán thời gian: {e}")
        raise

def generate_all_datetimes(base_date: datetime, rt) -> dict:
    try:
        period_id = rt.Period_ID
        return {
            "ActiveAt": calculate_datetime(base_date, rt.ActiveOffset, rt.ActiveOn, rt.ActiveAt, period_id),
            "DeactiveAt": calculate_datetime(base_date, rt.DeactiveOffset, rt.DeactiveOn, rt.DeactiveAt, period_id),
            "StartAt": calculate_datetime(base_date, rt.StartOffset, rt.StartOn, rt.StartAt, period_id),
            "EndAt": calculate_datetime(base_date, rt.EndOffset, rt.EndOn, rt.EndAt, period_id),
            "FromAt": calculate_datetime(base_date, rt.FromOffset, rt.FromOn, rt.From, period_id),
            "ToAt": calculate_datetime(base_date, rt.ToOffset, rt.ToOn, rt.To, period_id),
            "XaActiveAt": calculate_datetime(base_date, rt.XaActiveOffset, rt.XaActiveOn, rt.XaActiveAt, period_id) if rt.XaActiveAt else None,
            "XaDeactiveAt": calculate_datetime(base_date, rt.XaDeactiveOffset, rt.XaDeactiveOn, rt.XaDeactiveAt, period_id) if rt.XaDeactiveAt else None,
            "XaStartAt": calculate_datetime(base_date, rt.XaStartOffset, rt.XaStartOn, rt.XaStartAt, period_id) if rt.XaStartAt else None,
            "XaEndAt": calculate_datetime(base_date, rt.XaEndOffset, rt.XaEndOn, rt.XaEndAt, period_id) if rt.XaEndAt else None,
            "XaFromAt": calculate_datetime(base_date, rt.XaFromOffset, rt.XaFromOn, rt.XaFromAt, period_id) if rt.XaFromAt else None,
            "XaToAt": calculate_datetime(base_date, rt.XaToOffset, rt.XaToOn, rt.XaToAt, period_id) if rt.XaToAt else None,
        }
    except Exception as e:
        print(f"❌ Lỗi khi tạo tất cả các mốc thời gian: {e}")
        raise

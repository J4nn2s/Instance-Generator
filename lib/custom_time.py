from datetime import timedelta
class CustomTime:
    def __init__(self, hour: int, minute: int = 0):
        self.total_minutes: int = hour * 60 + minute

    def __add__(self, other) -> "CustomTime":
        if isinstance(other, timedelta):
            new_total_minutes: int = self.total_minutes + int(other.total_seconds()) // 60
            return CustomTime(new_total_minutes // 60, new_total_minutes % 60)
        return NotImplemented

    def __sub__(self, other) -> "CustomTime":
        if isinstance(other, timedelta):
            new_total_minutes = self.total_minutes - int(other.total_seconds()) // 60
            return CustomTime(new_total_minutes // 60, new_total_minutes % 60)
        return NotImplemented

    def to_24_hour_format(self) -> str:
        hours = self.total_minutes // 60
        minutes = self.total_minutes % 60
        return f"{hours:02}:{minutes:02}"
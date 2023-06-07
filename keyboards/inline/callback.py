from aiogram.filters.callback_data import CallbackData
from pydantic import Field


class DateCallbackData(CallbackData, prefix='date'):
    year: int = Field(default=None)
    month: int = Field(default=None, ge=1, le=12)
    day: int = Field(default=None, ge=0, le=31)


class TimeCallbackData(CallbackData, prefix='time'):
    hour: int = Field(default=None, le=23)
    minute: int = Field(default=None, le=59)
    action: str = None

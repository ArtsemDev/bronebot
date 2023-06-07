from calendar import Calendar
from datetime import date
from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import DateCallbackData


class GramDateInlineKeyboardMarkup(object):

    @classmethod
    async def create(cls, year: int = None, month: int = None) -> InlineKeyboardMarkup:
        if not all((year, month)):
            today = date.today()
        else:
            today = date(year=year, month=month, day=1)
        month = Calendar(firstweekday=0).monthdayscalendar(year=today.year, month=today.month)
        next_month = (today.month + 1) if today.month < 12 else 1
        next_year = today.year if today.month < 12 else (today.year + 1)
        prev_month = (today.month - 1) if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else (today.year - 1)

        buttons = [
            [
                InlineKeyboardButton(
                    text=today.strftime('%B %Y'),
                    callback_data=' '
                )
            ]
        ]

        buttons += [
            [
                InlineKeyboardButton(
                    text=f'{day}' if day else ' ',
                    callback_data=DateCallbackData(
                        year=today.year,
                        month=today.month,
                        day=day,
                    ).pack() if day else ' '
                )
                for day in week
            ]
            for week in month
        ]
        buttons += [
            [
                InlineKeyboardButton(
                    text='<-',
                    callback_data=DateCallbackData(
                        year=prev_year,
                        month=prev_month
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='->',
                    callback_data=DateCallbackData(
                        year=next_year,
                        month=next_month
                    ).pack()
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @classmethod
    async def parse(cls, callback_data: DateCallbackData) -> Union[date, InlineKeyboardMarkup]:
        if callback_data.day:
            return date(year=callback_data.year, month=callback_data.month, day=callback_data.day)
        else:
            return await cls.create(year=callback_data.year, month=callback_data.month)

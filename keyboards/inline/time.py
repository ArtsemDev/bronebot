from datetime import time
from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import TimeCallbackData


class GramTimeInlineKeyboardMarkup(object):

    @classmethod
    async def create(cls, hour: int = None, minute: int = None) -> InlineKeyboardMarkup:
        if hour is None and minute is None:
            selected_time = time(hour=19, minute=0)
        else:
            selected_time = time(hour=hour, minute=minute)
        buttons = [
            [
                InlineKeyboardButton(
                    text=f'+',
                    callback_data=TimeCallbackData(
                        hour=(selected_time.hour + 1) if selected_time.hour < 23 else 0,
                        minute=selected_time.minute
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='+',
                    callback_data=TimeCallbackData(
                        hour=selected_time.hour
                        if selected_time.minute < 55 else
                        selected_time.hour + 1
                        if selected_time.hour < 23
                        else 0,
                        minute=(selected_time.minute + 5) if selected_time.minute < 55 else 0
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{selected_time.hour}',
                    callback_data=' '
                ),
                InlineKeyboardButton(
                    text=f'{selected_time.minute}',
                    callback_data=' '
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'-',
                    callback_data=TimeCallbackData(
                        hour=(selected_time.hour - 1) if selected_time.hour > 0 else 23,
                        minute=selected_time.minute
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='-',
                    callback_data=TimeCallbackData(
                        hour=selected_time.hour
                        if selected_time.minute > 0 else
                        selected_time.hour - 1
                        if selected_time.hour > 0 else
                        23,
                        minute=(selected_time.minute - 5) if selected_time.minute > 0 else 55
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='SELECT',
                    callback_data=TimeCallbackData(
                        hour=selected_time.hour,
                        minute=selected_time.minute,
                        action='select'
                    ).pack()
                )
            ]
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @classmethod
    async def parse(cls, callback_data: TimeCallbackData) -> Union[time, InlineKeyboardMarkup]:
        if callback_data.action == 'select':
            return time(hour=callback_data.hour, minute=callback_data.minute)
        else:
            return await cls.create(hour=callback_data.hour, minute=callback_data.minute)

from datetime import datetime
from typing import Literal, Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import PositiveInt
from sqlalchemy import select

from utils.models import UserReservation


class ReservationCallbackData(CallbackData, prefix='reserv'):
    action: Optional[Literal[
        'mybook',
        'book',
        'delete'
    ]]
    reservation_id: Optional[PositiveInt]


reservation_panel_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🍽 БРОНЬ СТОЛИКА',
                callback_data=ReservationCallbackData(
                    action='book'
                ).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text='🍽 МОИ БРОНИ',
                callback_data=ReservationCallbackData(
                    action='mybook'
                ).pack()
            ),
        ]
    ]
)


async def reservation_list_ikb(user_id: int) -> InlineKeyboardMarkup:
    async with UserReservation.session() as session:
        reservations = await session.scalars(
            select(UserReservation)
            .filter(UserReservation.user_id == user_id, UserReservation.date_reservation > datetime.now())
        )
        buttons = [
            [
                InlineKeyboardButton(
                    text=f'{reservation.date_reservation.strftime("%d.%m.%y %H:%M")}',
                    callback_data=' '
                ),
                InlineKeyboardButton(
                    text='❌',
                    callback_data=ReservationCallbackData(
                        action='delete',
                        reservation_id=reservation.id
                    ).pack()
                ),
            ]
            for reservation in reservations
        ]
        return InlineKeyboardMarkup(
            inline_keyboard=buttons
        ) if buttons else None

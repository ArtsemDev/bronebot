from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_panel_rkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='ВЫБЕРИТЕ ДЕЙСТВИЕ НИЖЕ!',
    keyboard=[
        [
            KeyboardButton(
                text='🍽 БРОНЬ СТОЛИКА'
            ),
            KeyboardButton(
                text='🍪 МЕНЮ'
            ),
        ],
        [
            KeyboardButton(
                text='💵 МОЙ БАЛАНС'
            )
        ]
    ]
)

from aiogram import Bot, Dispatcher

from settings import SETTINGS


bot = Bot(
    token=SETTINGS.BOT_TOKEN.get_secret_value(),
    parse_mode='HTML'
)
dp = Dispatcher()

from handlers.router import router
from loader import bot, dp


dp.include_router(router=router)


if __name__ == '__main__':
    dp.run_polling(bot)

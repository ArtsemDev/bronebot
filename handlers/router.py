from aiogram import Router

from .users.handlers import router as users_router


router = Router()
router.include_router(router=users_router)

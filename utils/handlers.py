from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в АлмаДомБот!")

@router.message(Command("add"))
async def cmd_add(message: Message):
    await message.answer("Форма добавления объекта в разработке. Ожидайте!")

def register_handlers(dp):
    dp.include_router(router)

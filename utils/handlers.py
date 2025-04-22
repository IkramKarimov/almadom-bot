from aiogram import Router, types

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в AlmaDomBot!")

def register_handlers(dp):
    dp.include_router(router)
from aiogram import Router, types, F

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в AlmaDomBot!")

@router.message(F.text == "/add")
async def cmd_add(message: types.Message):
    await message.answer("Форма добавления объекта в разработке. Ожидайте!")
    
def register_handlers(dp):
    dp.include_router(router)

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в АлмаДомБот!")

@router.message(Command("add"))
async def cmd_add(message: Message):
    await message.answer("Форма добавления объекта в разработке. Ожидайте!")

def register_handlers(dp):
    dp.include_router(router)

@router.message(F.text == "Квартира")
async def start_flat_creation(message: Message, state: FSMContext):
    await state.set_state(FlatForm.district)
    await message.answer("Выберите район:", reply_markup=get_district_keyboard())
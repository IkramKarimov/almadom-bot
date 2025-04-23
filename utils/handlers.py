from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.keyboards import property_type_kb, get_district_keyboard
from utils.add_appartment_state import AddAppartment

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в АлмаДомБот!")
    
@router.message(F.text == "Добавить объект")
async def choose_property_type(message: Message):
    await message.answer("Выберите тип недвижимости:", reply_markup=property_type_kb)

def register_handlers(dp):
    dp.include_router(router)

@router.message(F.text == "Квартира")
async def start_flat_creation(message: Message, state: FSMContext):
    await state.set_state(FlatForm.district)
    await message.answer("Выберите район:", reply_markup=get_district_keyboard())
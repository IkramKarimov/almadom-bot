from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.keyboards import property_type_kb, get_district_keyboard
from utils.keyboards import property_type_kb, get_room_count_keyboard
from states.add_appartment_state import AddApartment

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в АлмаДомБот!")
    
@router.message(Command("add"))
async def choose_property_type(message: Message):
    await message.answer("Выберите тип недвижимости:", reply_markup=property_type_kb)

def register_handlers(dp):
    dp.include_router(router)

@router.message(F.text == "Квартира")
async def start_flat_creation(message: Message, state: FSMContext):
    await state.set_state(AddApartment.district)
    await message.answer("Выберите район:", reply_markup=get_district_keyboard())
    
@router.message(AddApartment.district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AddApartment.rooms)
    await message.answer("Сколько комнат?", reply_markup=get_room_count_keyboard())
    
@router.message(AddApartment.rooms)
async def ask_complex_name(message: Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(AddApartment.complex_name)
    await message.answer("Укажите название жилого комплекса (или напишите «-», если его нет):")
    
@router.message(AddApartment.complex_name)
async def ask_year_built(message: Message, state: FSMContext):
    text = message.text.strip()
    await state.update_data(complex_name=None if text == "-" else text)
    await state.set_state(AddApartment.year_built)
    await message.answer("Укажите год постройки:")
    
@router.message(AddApartment.year_built)
async def ask_price(message: Message, state: FSMContext):
    year = message.text.strip()
    if not year.isdigit():
        await message.answer("Пожалуйста, введите год числом.")
        return

    await state.update_data(year_built=int(year))
    await state.set_state(AddApartment.price)
    await message.answer("Укажите цену объекта (в тг):")
    
@router.message(AddApartment.price)
async def ask_area(message: Message, state: FSMContext):
    price_text = message.text.replace(" ", "").replace(",", "")
    if not price_text.isdigit():
        await message.answer("Пожалуйста, введите цену числом.")
        return

    await state.update_data(price=int(price_text))
    await state.set_state(AddApartment.area)
    await message.answer("Укажите площадь квартиры (в м²):")
    
@router.message(AddApartment.area)
async def ask_floor_info(message: Message, state: FSMContext):
    area_text = message.text.replace(",", ".").replace(" ", "")
    try:
        area = float(area_text)
    except ValueError:
        await message.answer("Пожалуйста, введите площадь числом.")
        return

    await state.update_data(area=area)
    await state.set_state(AddApartment.floor_info)
    await message.answer("Укажите этаж / этажность (например: 3/9):")
    
    @router.message(AddApartment.floor_info)
async def ask_media(message: Message, state: FSMContext):
    await state.update_data(floor_info=message.text)
    await state.set_state(AddApartment.media)
    await message.answer("Теперь отправьте фото или видео объекта. Когда закончите, нажмите /done.")
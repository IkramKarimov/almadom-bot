from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.add_apartment_state import AddApartment

router = Router()

@router.message(F.text == "Квартира")
async def start_add_apartment(message: types.Message, state: FSMContext):
    await state.set_state(AddApartment.district)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Алмалинский"), types.KeyboardButton(text="Бостандыкский")],
            [types.KeyboardButton(text="Медеуский"), types.KeyboardButton(text="Наурызбайский")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите район:", reply_markup=keyboard)

@router.message(AddApartment.district)
async def process_district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AddApartment.rooms)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="1"), types.KeyboardButton(text="2")],
            [types.KeyboardButton(text="3"), types.KeyboardButton(text="4+")],
        ],
        resize_keyboard=True
    )
    await message.answer("Сколько комнат в квартире?", reply_markup=keyboard)

@router.message(AddApartment.rooms)
async def process_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(AddApartment.complex_name)

    await message.answer("Укажите название ЖК (если есть) или напишите '-' (если нет):", reply_markup=types.ReplyKeyboardRemove())
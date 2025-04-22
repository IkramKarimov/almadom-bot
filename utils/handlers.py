
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()


class AddProperty(StatesGroup):
    choosing_type = State()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в AlmaDomBot!")


@router.message(F.text == "/add")
async def cmd_add(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Квартира"),
            KeyboardButton(text="Дом")
        ], [
            KeyboardButton(text="Таунхаус"),
            KeyboardButton(text="Коммерческая недвижимость")
        ], [
            KeyboardButton(text="Участок")
        ]],
        resize_keyboard=True
    )
    await message.answer("Выберите тип недвижимости:", reply_markup=keyboard)
    await state.set_state(AddProperty.choosing_type)


@router.message(AddProperty.choosing_type)
async def property_type_chosen(message: types.Message, state: FSMContext):
    await state.update_data(property_type=message.text)
    await message.answer(f"Вы выбрали: {message.text}", reply_markup=ReplyKeyboardRemove())
    # Следующий шаг будет добавлен позже

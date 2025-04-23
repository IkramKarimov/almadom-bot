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
    
from datetime import datetime

@router.message(AddApartment.year_built)
async def process_year_built(message: Message, state: FSMContext):
    year = message.text.strip()

    if not year.isdigit() or not (1900 <= int(year) <= datetime.now().year):
        await message.answer("Пожалуйста, введите корректный год постройки (от 1900 до текущего).")
        return

    await state.update_data(year_built=int(year))
    await message.answer("Введите цену (только число, без пробелов):")
    await state.set_state(AddApartment.price)
    
@router.message(AddApartment.price)
async def process_price(message: Message, state: FSMContext):
    price = message.text.replace(" ", "").strip()

    if not price.isdigit() or int(price) <= 0:
        await message.answer("Пожалуйста, введите корректную цену (только число, больше нуля).")
        return

    await state.update_data(price=int(price))
    await message.answer("Введите общую площадь (в квадратных метрах, например 78.5):")
    await state.set_state(AddApartment.area)
    
@router.message(AddApartment.area)
async def process_area(message: Message, state: FSMContext):
    area = message.text.replace(",", ".").strip()

    try:
        area_value = float(area)
        if area_value <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректную площадь (например 78.5).")
        return

    await state.update_data(area=area_value)
    await message.answer("Введите этаж (например 5):")
    await state.set_state(AddApartment.floor)
    
@router.message(AddApartment.floor)
async def process_floor(message: Message, state: FSMContext):
    text = message.text.strip()

    if "/" in text:
        parts = text.split("/")
    elif " " in text:
        parts = text.split()
    else:
        await message.answer("Введите этаж и этажность через / или пробел, например: 5/9 или 5 9")
        return

    if len(parts) != 2:
        await message.answer("Пожалуйста, введите два числа — этаж и этажность.")
        return

    try:
        floor = int(parts[0])
        total_floors = int(parts[1])
        if floor <= 0 or total_floors <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Оба значения должны быть положительными числами.")
        return

    await state.update_data(floor=floor, total_floors=total_floors)
    await message.answer("Отправьте фото или видео объекта (можно несколько). Когда закончите — нажмите 'Готово'.")
    await state.set_state(AddApartment.media)
    
    @router.message(AddApartment.media, F.photo | F.video)
async def handle_media(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])

    if message.photo:
        media.append(message.photo[-1].file_id)
    elif message.video:
        media.append(message.video.file_id)

    await state.update_data(media=media)
    await message.answer("Добавлено. Можете отправить ещё или нажмите 'Готово'.")

@router.message(AddApartment.media, F.text.lower() == "готово")
async def finish_media_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])

    if not media:
        await message.answer("Вы не добавили ни одного файла. Отправьте хотя бы одно фото или видео.")
        return

    await message.answer("Спасибо! Все данные собраны. Скоро объект будет опубликован.")
    await state.clear()

    # Здесь можно добавить отправку заявки в канал и админу
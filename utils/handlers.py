from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Contact, InputMediaPhoto, InputMediaVideo
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.add_appartment_state import AddApartment, EditFieldState
from utils.keyboards import (
    property_type_kb, 
    get_district_keyboard, 
    get_room_count_keyboard,
    get_preview_keyboard, 
    edit_fields_keyboard,
    get_contact_keyboard,
    done_keyboard
)
from utils.format_summary import format_summary
from config import CHANNEL_ID

router = Router()

# Читабельные имена полей
FIELD_NAMES = {
    "district": "Район",
    "rooms": "Количество комнат",
    "complex_name": "Жилой комплекс",
    "address": "Адрес",
    "year_built": "Год постройки",
    "price": "Цена",
    "area": "Площадь",
    "floor_info": "Этажность",
    "media": "Медиа",
}

### --- Стартовые команды --- ###

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в АлмаДомБот!")

@router.message(Command("add"))
async def choose_property_type(message: Message):
    await message.answer("Выберите тип недвижимости:", reply_markup=property_type_kb)

@router.message(F.text == "Квартира")
async def start_flat_creation(message: Message, state: FSMContext):
    await state.set_state(AddApartment.district)
    await message.answer("Выберите район:", reply_markup=get_district_keyboard())

### --- Основные этапы заполнения квартиры --- ###

@router.message(AddApartment.district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AddApartment.rooms)
    await message.answer("Сколько комнат?", reply_markup=get_room_count_keyboard())

@router.message(AddApartment.rooms)
async def ask_complex_name(message: Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(AddApartment.complex_name)
    await message.answer("Укажите название ЖК (или напишите «-», если его нет):")

@router.message(AddApartment.complex_name)
async def ask_address(message: Message, state: FSMContext):
    text = message.text.strip()
    await state.update_data(complex_name=None if text == "-" else text)
    await state.set_state(AddApartment.address)
    await message.answer("Укажите адрес объекта:")

@router.message(AddApartment.address)
async def ask_year_built(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(AddApartment.year_built)
    await message.answer("Укажите год постройки:")

@router.message(AddApartment.year_built)
async def ask_price(message: Message, state: FSMContext):
    year = message.text.strip()
    if not year.isdigit():
        await message.answer("Введите год числом.")
        return
    await state.update_data(year_built=int(year))
    await state.set_state(AddApartment.price)
    await message.answer("Укажите цену в тенге:")

@router.message(AddApartment.price)
async def ask_area(message: Message, state: FSMContext):
    price_text = message.text.replace(" ", "").replace(",", "")
    if not price_text.isdigit():
        await message.answer("Введите цену числом.")
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
        await message.answer("Введите площадь числом.")
        return
    await state.update_data(area=area)
    await state.set_state(AddApartment.floor_info)
    await message.answer("Укажите этаж/этажность (например 3/9):")

@router.message(AddApartment.floor_info)
async def ask_media(message: Message, state: FSMContext):
    await state.update_data(floor_info=message.text)
    await state.set_state(AddApartment.media)
    await message.answer("Отправьте фото или видео объекта. Когда закончите — нажмите «Готово».", reply_markup=done_keyboard)

@router.message(AddApartment.media, F.photo | F.video)
async def collect_media(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    media.append(file_id)
    await state.update_data(media=media)
    await message.answer("Файл добавлен. Отправьте ещё или нажмите «Готово».", reply_markup=done_keyboard)

@router.message(AddApartment.media, F.text.lower() == "готово")
async def preview_listing(message: Message, state: FSMContext):
    data = await state.get_data()

    preview_text = format_summary(data)
    
    media = data.get("media", [])
    media_group = [
        InputMediaPhoto(file_id) if file_id.startswith("AgAC") else InputMediaVideo(file_id)
        for file_id in media
    ]

    if media_group:
        await message.answer_media_group(media_group)

    await message.answer(preview_text, reply_markup=get_preview_keyboard())

### --- Работа с предпросмотром --- ###

@router.callback_query(F.data == "publish")
async def publish_object(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    media_group = [
        InputMediaPhoto(file_id) if file_id.startswith("AgAC") else InputMediaVideo(file_id)
        for file_id in data.get("media", [])
    ]

    if media_group:
        await callback.bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

    post_text = format_summary(data)
    await callback.bot.send_message(chat_id=CHANNEL_ID, text=post_text)

    await callback.message.answer("Объявление опубликовано!")
    await state.clear()

@router.callback_query(F.data == "edit")
async def choose_edit_field(callback: CallbackQuery):
    await callback.message.answer("Выберите, что хотите изменить:", reply_markup=edit_fields_keyboard())

@router.callback_query(F.data == "cancel")
async def cancel_object(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Добавление объекта отменено.")

### --- Редактирование выбранного поля --- ###

@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace("edit_", "")
    await state.update_data(edit_field=field)

    if field == "district":
        await callback.message.answer("Выберите новый район:", reply_markup=get_district_keyboard())
    elif field == "rooms":
        await callback.message.answer("Выберите количество комнат:", reply_markup=get_room_count_keyboard())
    else:
        readable_name = FIELD_NAMES.get(field, field)
        await callback.message.answer(f"Введите новое значение для поля: {readable_name}")

    await state.set_state(EditFieldState.new_value)

@router.message(EditFieldState.new_value)
async def process_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("edit_field")
    new_value = message.text

    if field == "year_built" or field == "price":
        if not new_value.isdigit():
            await message.answer("Пожалуйста, введите число.")
            return
        new_value = int(new_value)

    elif field == "area":
        try:
            new_value = float(new_value.replace(",", "."))
        except ValueError:
            await message.answer("Пожалуйста, введите площадь числом.")
            return

    await state.update_data({field: new_value, "edit_field": None})
    await state.set_state(AddApartment.media)  # возвращаемся к предпросмотру

    updated_data = await state.get_data()
    summary = format_summary(updated_data)
    await message.answer(f"Данные обновлены:\n\n{summary}", reply_markup=get_preview_keyboard())

### --- Контакт для связи --- ###

@router.callback_query(F.data == "confirm_publish")
async def confirm_publish(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Отправьте ваш контакт для связи:", reply_markup=get_contact_keyboard())
    await state.set_state(AddApartment.contact)

@router.message(AddApartment.contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    await message.answer("Контакт получен, объект отправлен на модерацию!")
    await state.clear()

### --- Обработка случайных сообщений вне контекста --- ###

@router.message()
async def fallback(message: Message):
    await message.answer("Пожалуйста, используйте команды /add или /start.")
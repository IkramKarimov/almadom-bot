from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Contact, InputMediaPhoto, InputMediaVideo
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
from config import CHANNEL_ID
from utils.keyboards import (start_menu_keyboard,
    property_type_kb, 
    get_district_keyboard,
    get_room_count_keyboard,
    get_preview_keyboard,
    edit_fields_keyboard,
    confirm_post_kb,
    add_more_media_keyboard,
    get_contact_keyboard,
    done_keyboard,
)
from utils.format_summary import format_summary

from states.add_appartment_state import AddApartment, EditFieldState

FIELD_NAMES = {
    "district": "Район",
    "rooms": "Количество комнат",
    "complex_name": "Жилой комплекс",
    "address": "Адрес",
    "year_built": "Год постройки",
    "price": "Цена",
    "area": "Площадь",
    "floor": "Этажность",
    "media": "Медиа",
}

router = Router()

from aiogram import F

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("draft"):
        await message.answer(
            "У вас есть незаконченный объект. Хотите продолжить?",
            reply_markup=continue_draft_kb
        )
    else:
        await state.clear()
        await message.answer(
        "👋 Добро пожаловать в <b>АлмаДомБот</b>!\n\n"
        "Что вы хотите сделать?",
        reply_markup=start_menu_keyboard(),
        parse_mode="HTML"
        )

@router.callback_query(F.data == "start")
async def cmd_start_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "👋 Добро пожаловать в <b>АлмаДомБот</b>!\n\n"
        "Что вы хотите сделать?",
        reply_markup=start_menu_keyboard(),
        parse_mode="HTML"
    )
    
@router.callback_query(F.data == "add_property")
async def process_add_property(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выберите тип недвижимости:",
        reply_markup=property_type_kb  # <-- твоя клавиатура выбора типа объекта
    )

@router.callback_query(F.data == "help")
async def process_help(callback: CallbackQuery):
    await callback.message.answer(
        "ℹ️ Если вам нужна помощь, обратитесь к нашему администратору: @ikramkir\n\n"
        "Или напишите сюда ваш вопрос!",
        parse_mode="HTML"
    )

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
async def ask_address(message: Message, state: FSMContext):
    text = message.text.strip()
    await state.update_data(complex_name=None if text == "-" else text)
    await state.set_state(AddApartment.address)
    await message.answer("Укажите адрес (улица или микрорайон, номер дома, пересечение с улицей при наличии):")
    
@router.message(AddApartment.address)
async def ask_year_built(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
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
    await message.answer("Теперь отправьте фото или видео объекта. Когда закончите, нажмите «Готово».", reply_markup=done_keyboard)

# Загрузка медиа
@router.message(AddApartment.media, F.content_type.in_({'photo', 'video'}))
async def process_new_media_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    media_group = data.get('media_group', [])

    if message.photo:
        file_id = message.photo[-1].file_id
        media_group.append({"type": "photo", "file_id": file_id})
    elif message.video:
        file_id = message.video.file_id
        media_group.append({"type": "video", "file_id": file_id})

    await state.update_data(media_group=media_group)
    await message.answer("Файл добавлен. Отправьте еще или нажмите «Готово», если закончили.", reply_markup=done_keyboard)
    
@router.callback_query(lambda c: c.data == "add_more_media")
async def add_more_media(callback: CallbackQuery):
    await callback.message.answer("Отправьте ещё фото или видео.")

@router.message(AddApartment.media, F.text.lower() == "✅ готово")
async def done_from_button(message: Message, state: FSMContext):
    await preview_listing(message, state)
    
# Здесь будет следующий шаг — предварительный просмотр
import logging
logger = logging.getLogger(__name__)

@router.message(AddApartment.media, F.text == "Готово")
async def preview_listing(message: Message, state: FSMContext):
    data = await state.get_data()
    media_files = data.get('media', [])  # исправил на правильный ключ 'media'
    
    media_group = []
    for file_id in media_files:
        if file_id.startswith("AgAC"):  # Фото
            media_group.append(InputMediaPhoto(media=file_id))
        elif file_id.startswith("BAAC") or file_id.startswith("DQAC"):  # Видео
            media_group.append(InputMediaVideo(media=file_id))

    preview_text = (
        f"<b>Предпросмотр квартиры:</b>\n"
        f"<b>Район:</b> {data.get('district')}\n"
        f"<b>Количество комнат:</b> {data.get('rooms')}\n"
        f"<b>Площадь:</b> {data.get('area')} м²\n"
        f"<b>Год постройки:</b> {data.get('year_built')}\n"
        f"<b>ЖК:</b> {data.get('complex_name', '—')}\n"
        f"<b>Адрес:</b> {data.get('address')}\n"
        f"<b>Этажность:</b> {data.get('floor_info', '—')}\n"
        f"<b>Цена:</b> {format(data.get('price'), ',').replace(',', ' ')} ₸"
    )

    if media_group:
        await message.answer_media_group(media_group)

    await message.answer(preview_text, reply_markup=get_preview_keyboard())

# ====== ПОДТВЕРЖДЕНИЕ ПУБЛИКАЦИИ ======
@router.callback_query(F.data == "confirm_publish")
async def confirm_publish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        "Отлично! Теперь отправьте ваш контакт для связи.",
        reply_markup=get_contact_keyboard()
    )
    await state.set_state(AddApartment.contact)

# ====== ПОЛУЧЕНИЕ КОНТАКТА И ПУБЛИКАЦИЯ ======
@router.message(AddApartment.contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data(contact=contact)

    data = await state.get_data()

    # Формируем текст поста
    post_text = (
        f"<b>🏡 Новое объявление:</b>\n"
        f"📍 <b>Район:</b> {data.get('district')}\n"
        f"🛏 <b>Комнаты:</b> {data.get('rooms')}\n"
        f"📐 <b>Площадь:</b> {data.get('area')} м²\n"
        f"🏗 <b>Год постройки:</b> {data.get('year_built')}\n"
        f"🏢 <b>ЖК:</b> {data.get('complex_name', '—')}\n"
        f"📫 <b>Адрес:</b> {data.get('address')}\n"
        f"🏢 <b>Этажность:</b> {data.get('floor_info')}\n"
        f"💰 <b>Цена:</b> {format(data.get('price'), ',').replace(',', '.')} ₸\n"
        f"☎️ <b>Контакт:</b> {contact}"
    )

    # Формируем медиагруппу
    media_group = []
    for media in data.get("media_group", []):
        if media["type"] == "photo":
            media_group.append(InputMediaPhoto(media=media["file_id"]))
        elif media["type"] == "video":
            media_group.append(InputMediaVideo(media=media["file_id"]))

    # Публикация в канал
    if media_group:
        await message.bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
    
    await message.bot.send_message(chat_id=CHANNEL_ID, text=post_text)

    # Ответ пользователю
    await message.answer("Объявление опубликовано! Спасибо.")
    await state.clear()

# Выбор "Редактировать"
@router.callback_query(F.data == "edit")
async def edit_object(callback: CallbackQuery):
    await callback.message.answer("Выберите поле для редактирования:", reply_markup=edit_fields_keyboard())

# Обработка выбора поля для редактирования
@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace("edit_", "")
    await state.update_data(edit_field=field)  # сохраняем текущее поле для редактирования

    if field == "district":
        await callback.message.answer("Выберите новый район:", reply_markup=get_district_keyboard())
    elif field == "rooms":
        await callback.message.answer("Выберите количество комнат:", reply_markup=get_room_count_keyboard())
    elif field == "year_built":
        await callback.message.answer("Введите новый год постройки (например, 2020):")
        await state.set_state(EditFieldState.new_value)
    elif field == "price":
        await callback.message.answer("Введите новую цену:")
        await state.set_state(EditFieldState.new_value)
    elif field == "area":
        await callback.message.answer("Введите новую площадь:")
        await state.set_state(EditFieldState.new_value)
    elif field == "floor_info":
        await callback.message.answer("Введите новую этажность (например, 5/9):")
        await state.set_state(EditFieldState.new_value)
    elif field == "complex_name":
        await callback.message.answer("Введите новый ЖК (или напишите '-' если нет):")
        await state.set_state(EditFieldState.new_value)
    elif field == "address":
        await callback.message.answer("Введите новый адрес:")
        await state.set_state(EditFieldState.new_value)
    elif field == "media":
        await callback.message.answer("Отправьте новые фото или видео объекта:")
        # Допустим для медиа другая логика обработки
    else:
        await callback.message.answer(f"Введите новое значение для поля: {field}")
        await state.set_state(EditFieldState.new_value)

# Обработка нового значения после ввода
@router.message(EditFieldState.new_value)
async def process_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("edit_field")  # правильно достаём
    new_value = message.text

    # Обновляем данные
    await state.update_data({field: new_value})

    # Возвращаемся к предпросмотру
    updated_data = await state.get_data()
    summary = format_summary(updated_data)
    await message.answer("Обновлено!\n\n" + summary, reply_markup=get_preview_keyboard())

    # Очищаем промежуточное состояние
    await state.set_state(AddApartment.confirm)

@router.callback_query(F.data == "cancel")
async def cancel_object(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Добавление объекта отменено.")

def register_handlers(dp):
    dp.include_router(router)
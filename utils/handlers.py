from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.keyboards import (property_type_kb, 
    get_district_keyboard,
    get_room_count_keyboard,
    get_preview_keyboard,
    get_contact_keyboard,
    done_keyboard,
)
from states.add_appartment_state import AddApartment

router = Router()

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
    
from utils.keyboards import done_keyboard

@router.message(AddApartment.floor_info)
async def ask_media(message: Message, state: FSMContext):
    await state.update_data(floor_info=message.text)
    await state.set_state(AddApartment.media)
    await message.answer("Теперь отправьте фото или видео объекта. Когда закончите, нажмите «Готово».", reply_markup=done_keyboard)

@router.message(AddApartment.media, F.photo | F.video)
async def collect_media(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    media.append(file_id)
    
    await state.update_data(media=media)
    await message.answer("Файл добавлен. Отправьте еще или нажмите «Готово», если закончили.", reply_markup=done_keyboard)
            
@router.message(AddApartment.floor_info)
async def ask_media(message: Message, state: FSMContext):
    await state.update_data(floor_info=message.text)
    await state.set_state(AddApartment.media)
    await message.answer("Теперь отправьте фото или видео объекта. Когда закончите, нажмите «Готово».", reply_markup=done_keyboard)
    
@router.message(AddApartment.media, F.photo | F.video)
async def collect_media(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    media.append(file_id)
    
    await state.update_data(media=media)
    await message.answer("Файл добавлен. Отправьте еще или нажмите \"Готово\", если закончили.")
    
@router.message(AddApartment.media, F.text.lower() == "готово")
async def done_from_button(message: Message, state: FSMContext):
    await preview_listing(message, state)
    
# Здесь будет следующий шаг — предварительный просмотр
    
from utils.keyboards import property_type_kb, get_district_keyboard, get_preview_keyboard

import logging
logger = logging.getLogger(__name__)

@router.message(AddApartment.media, F.text == "Готово")
async def preview_listing(message: Message, state: FSMContext):
    data = await state.get_data()

    preview_text = (
        f"<b>Предпросмотр квартиры:</b>\n"
        f"<b>Район:</b> {data.get('district')}\n"
        f"<b>Количество комнат:</b> {data.get('rooms')}\n"
        f"<b>Площадь:</b> {data.get('area')} м²\n"
        f"<b>Год постройки:</b> {data.get('year_built')}\n"
        f"<b>ЖК:</b> {data.get('complex_name', '—')}\n"
        f"<b>Этажность:</b> {data.get('floor_info', '—')}\n"
        f"<b>Цена:</b> {format(data.get('price'), ',').replace(',', '.')} ₸"
    )

    from aiogram.types import InputMediaPhoto, InputMediaVideo

    media = data.get("media", [])
    media_group = []

    for file_id in media:
        if file_id.startswith("AgAC"):  # Фото
            media_group.append(InputMediaPhoto(media=file_id))
        elif file_id.startswith("BAAC") or file_id.startswith("DQAC"):  # Видео
            media_group.append(InputMediaVideo(media=file_id))

    if media_group:
        await message.answer_media_group(media_group)

    await message.answer(preview_text, reply_markup=get_preview_keyboard())
    
from aiogram import types

from utils.keyboards import get_contact_keyboard

@router.callback_query(lambda c: c.data == "confirm_publish")
async def confirm_publish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        "Отлично! Теперь отправьте ваш контакт для связи.",
        reply_markup=get_contact_keyboard()
    )
    await state.set_state(AddApartment.contact)

@router.callback_query(lambda c: c.data == "cancel_publish")
async def cancel_publish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Публикация отменена. Чтобы начать заново, нажмите /add.")
    await state.clear()
    
from aiogram.types import Contact, InputMediaPhoto, InputMediaVideo
from config import CHANNEL_ID

@router.message(AddApartment.contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data(contact=contact)

    data = await state.get_data()
    # Здесь можно сформировать и отправить финальное сообщение в канал или администратору
    await message.answer("Контакт получен, объект отправлен на модерацию!")
    await state.clear()

    post_text = (
        f"<b>Новое объявление:</b>\n"
        f"<b>Район:</b> {data.get('district')}\n"
        f"<b>Комнаты:</b> {data.get('rooms')}\n"
        f"<b>Площадь:</b> {data.get('area')} м²\n"
        f"<b>Год постройки:</b> {data.get('year_built')}\n"
        f"<b>ЖК:</b> {data.get('complex_name', '—')}\n"
        f"<b>Этажность:</b> {data.get('floor_info')}\n"
        f"<b>Цена:</b> {data.get('price')} ₸\n"
        f"<b>Контакт:</b> {contact}"
    )

    media_group = []
    for file_id in data.get("media", []):
        if file_id.startswith("AgAC"):  # Фото
            media_group.append(InputMediaPhoto(media=file_id))
        elif file_id.startswith("BAAC") or file_id.startswith("DQAC"):  # Видео
            media_group.append(InputMediaVideo(media=file_id))

    if media_group:
        await message.bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

    await message.bot.send_message(chat_id=CHANNEL_ID, text=post_text)

    await message.answer("Объявление опубликовано! Спасибо.")
    await state.clear()
    
def register_handlers(dp):
    dp.include_router(router)
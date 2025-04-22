from aiogram import types, Dispatcher
from aiogram.types import InputMediaPhoto
from config import CHANNEL_ID
from utils.watermark import add_watermark
import os

user_sessions = {}

async def start_command(message: types.Message):
    await message.answer("Привет! Напиши /add чтобы добавить объект недвижимости.")

async def add_command(message: types.Message):
    user_sessions[message.from_user.id] = {'step': 'type'}
    await message.answer("Выберите тип недвижимости: Квартира, Дом, Таунхаус, Коммерческая недвижимость, Участок")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(add_command, commands="add")

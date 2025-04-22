import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
import os

from utils.handlers import register_handlers

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# ВАЖНО: dispatcher передается первым аргументом
setup_application(app, dispatcher=dp, bot=bot)

if __name__ == "__main__":
    web.run_app(app, port=8000)

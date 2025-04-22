import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import setup_application

from utils.handlers import register_handlers

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
register_handlers(dp)

async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook set")

async def on_shutdown(app):
    await bot.delete_webhook()
    print("Webhook removed")

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# 👇 Здесь просто вызываем setup_application — он сам добавит нужный маршрут
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    web.run_app(app, port=8000)

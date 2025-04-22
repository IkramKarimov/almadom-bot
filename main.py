import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from utils.handlers import register_handlers
from config import BOT_TOKEN, APP_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def on_startup(app):
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    print("Webhook deleted")

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/{BOT_TOKEN}")

if __name__ == "__main__":
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
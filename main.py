
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from handlers import router
from config import TOKEN, WEBHOOK_URL

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_routes([
    web.post(f"/{TOKEN}", setup_application(app=app, dispatcher=dp, bot=bot)),
])

if __name__ == "__main__":
    web.run_app(app, port=8000)

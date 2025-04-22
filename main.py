import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
import os

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN, default=Bot.DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def on_startup(app: web.Application):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

app = web.Application()
app.on_startup.append(on_startup)
app.router.add_routes([web.post(f'/{TOKEN}', setup_application(app, dp, bot=bot))])

if __name__ == '__main__':
    web.run_app(app, port=8000)

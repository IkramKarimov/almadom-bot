import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import TOKEN, WEBHOOK_URL
from config import WEB_SERVER_HOST, WEB_SERVER_PORT

from utils.handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(app: web.Application):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    logger.info("Webhook установлен.")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logger.info("Webhook удален.")

def create_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Регистрируем вебхуки для Telegram
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/{TOKEN}")
    
    return app

if __name__ == "__main__":
    try:
        logger.info("Запуск веб-приложения...")
        web.run_app(create_app(), host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
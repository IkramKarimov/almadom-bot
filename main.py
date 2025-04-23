import asyncio
import logging
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from handlers import router
from config import TOKEN, WEBHOOK_URL

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(app: web.Application) -> None:
    """Функция запуска приложения."""
    try:
        await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        logger.info("Webhook успешно установлен.")
    except Exception as e:
        logger.error(f"Ошибка при установке webhook: {e}")

async def on_shutdown(app: web.Application) -> None:
    """Функция остановки приложения."""
    try:
        await bot.delete_webhook()
        logger.info("Webhook успешно удален.")
    except Exception as e:
        logger.error(f"Ошибка при удалении webhook: {e}")

def create_app() -> web.Application:
    """Создание и настройка веб-приложения."""
    app = web.Application()
    # Правильный вызов setup_application:
app = setup_application(app=app, dispatcher=dp, bot=bot)

# Устанавливаем webhook
async def on_startup(app: web.Application):
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_routes([
        web.post(f"/{TOKEN}", setup_application(app=app, dispatcher=dp, bot=bot)),
    ])

    return app

if __name__ == "__main__":
    try:
        logger.info("Запуск веб-приложения...")
        app = create_app()
        web.run_app(app, port=8000)
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
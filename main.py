import logging
import asyncio
from aiohttp import web
from aiogram.types import Update
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT
from utils.handlers import router

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

# Webhook handler
async def handle_webhook(request):
    body = await request.text()
    update = Update.model_validate_json(body)
    await dp.feed_update(bot, update)
    return web.Response()

# Запуск бота
async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info("Webhook установлен")

async def on_shutdown(app):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

#async def main():
    #logger.info("Удаление Webhook перед запуском polling")
    #await bot.delete_webhook(drop_pending_updates=True)

    #logger.info("Бот запущен в режиме polling")
    #await dp.start_polling(bot)

#if __name__ == "__main__":
    #try:
        #asyncio.run(main())
    #except (KeyboardInterrupt, SystemExit):
        #logger.info("Бот остановлен.")

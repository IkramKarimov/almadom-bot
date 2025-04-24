
import os

TOKEN = os.getenv("BOT_TOKEN")  # или просто строкой: 'your_token_here'
WEBHOOK_URL = "https://almadom-bot.onrender.com"
WEBHOOK_PATH = f"/{TOKEN}"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", default=8000))

CHANNEL_ID = "@almadom_channel"


import os

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://almadom-bot.onrender.com") #("https://almadom-bot-production-3cb4.up.railway.app").rstrip("/")
WEBHOOK_PATH = f"/{TOKEN}"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", default=8000))

CHANNEL_ID = "@almadomchannel"

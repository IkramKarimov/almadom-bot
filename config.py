
import os

TOKEN = os.getenv("TOKEN", "7513357606:AAEiNTAuIVn3CL_-txzYIl2Pa7VSVzHRFwQ")  # или просто строкой: 'your_token_here'
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = f"/{TOKEN}"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", default=8000))

CHANNEL_ID = "@almadomchannel"

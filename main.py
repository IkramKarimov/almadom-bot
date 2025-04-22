from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'AlmaDomBot is running'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        if text == '/start':
            bot.send_message(chat_id=chat_id, text='Привет! Я АлмаДомБот — бот для подачи и фильтрации объектов')
    return 'ok'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

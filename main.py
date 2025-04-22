from flask import Flask, request
import telegram

TOKEN = '7513357606:AAEiNTAuIVn3CL_-txzYIl2Pa7VSVzHRFwQ'
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.text == '/start':
        chat_id = update.message.chat.id
        bot.send_message(chat_id=chat_id, text='Привет! Я АлмаДомБот — бот для подачи и фильтрации объектов')
    return 'ok'

@app.route('/')
def home():
    return 'Бот работает!'

if __name__ == '__main__':
    app.run()

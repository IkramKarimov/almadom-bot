from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

done_upload_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Готово")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
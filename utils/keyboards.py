from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

done_upload_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Готово")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_post_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="confirm_post")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_post")]
    ]
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора типа недвижимости
property_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Квартира")],
        [KeyboardButton(text="Дом")],
        [KeyboardButton(text="Таунхаус")],
        [KeyboardButton(text="Коммерческая недвижимость")],
        [KeyboardButton(text="Участок")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура выбора района
def get_district_keyboard():
    districts = [
        "Алатауский", "Алмалинский", "Ауэзовский",
        "Бостандыкский", "Жетысуский", "Медеуский",
        "Наурызбайский", "Турксибский"
    ]
    keyboard = [[KeyboardButton(text=d)] for d in districts]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
# Клавиатура выбора количества комнат
def get_room_count_keyboard():
    buttons = [
        [KeyboardButton(text="1"), KeyboardButton(text="2")],
        [KeyboardButton(text="3"), KeyboardButton(text="4+")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

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

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_preview_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_publish")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_publish")]
    ])
    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить контакт", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
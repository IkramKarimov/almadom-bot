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
    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

done_keyboard = ReplyKeyboardMarkup(
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

# Клавиатура предпросмотра
def get_preview_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_publish")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_publish")]
    ])
    
# Клавиатура редактирования полей
def edit_fields_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Тип недвижимости", callback_data="edit:type")],
        [InlineKeyboardButton(text="Район", callback_data="edit:district")],
        [InlineKeyboardButton(text="Количество комнат", callback_data="edit:rooms")],
        [InlineKeyboardButton(text="ЖК", callback_data="edit:complex_name")],
        [InlineKeyboardButton(text="Адрес", callback_data="edit:address")],
        [InlineKeyboardButton(text="Год постройки", callback_data="edit:year")],
        [InlineKeyboardButton(text="Цена", callback_data="edit:price")],
        [InlineKeyboardButton(text="Площадь", callback_data="edit:area")],
        [InlineKeyboardButton(text="Этажность", callback_data="edit:floor")],
        [InlineKeyboardButton(text="Медиафайлы", callback_data="edit:media")],
        [InlineKeyboardButton(text="Назад", callback_data="edit:back_to_preview")]
    ])
    
# Клавиатура отправки контакта
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить контакт", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
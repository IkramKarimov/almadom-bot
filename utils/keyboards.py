from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора типа недвижимости
property_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Квартира")],
        [KeyboardButton(text="Дом")],
        [KeyboardButton(text="Таунхаус")],
        [KeyboardButton(text="Коммерческая недвижимость")],
        [KeyboardButton(text="Участок")],
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
    
# Клавиатура "Готово"
done_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Готово")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

confirm_post_kb = ReplyKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="confirm_post")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_post")]
    ]
)

# Клавиатура предпросмотра
def get_preview_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_publish")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_publish")]
    ])
    
# Клавиатура редактирования полей
def edit_fields_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Тип недвижимости", callback_data="edit_type")
        ],
        [
            InlineKeyboardButton(text="📍 Район", callback_data="edit_district"),
            InlineKeyboardButton(text="🛏️ Комнаты", callback_data="edit_rooms"),
        ],
        [
            InlineKeyboardButton(text="📐 Площадь", callback_data="edit_area"),
            InlineKeyboardButton(text="📆 Год постройки", callback_data="edit_year_built"),
        ],
        [
            InlineKeyboardButton(text="Этажность", callback_data="edit_floor_info"),
            InlineKeyboardButton(text="Цена", callback_data="edit_price"),
        ],
        [
            InlineKeyboardButton(text="ЖК", callback_data="edit_complex_name"),
            InlineKeyboardButton(text="Адрес", callback_data="edit_address"),
        ],
        [
            InlineKeyboardButton(text="Фото/Видео", callback_data="edit_media"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_preview"),
        ]
    ])
    return keyboard
    
# Клавиатура добавления еще фото
def add_more_media_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить ещё фото/видео", callback_data="add_more_media")],
        [InlineKeyboardButton(text="✅ Готово", callback_data="done_uploading")]
    ])
    return keyboard
    
# Клавиатура отправки контакта
def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить контакт", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
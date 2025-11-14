from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить пользователя")],
        [KeyboardButton(text="Удалить пользователя")],
        [KeyboardButton(text="Текущий список пользователей")],
        [KeyboardButton(text="Основное меню")],
    ],
    resize_keyboard=True,   # кнопки подгоняются по ширине экрана
    one_time_keyboard=False # клавиатура не скрывается после нажатия
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Alerts за 3 дня")],
        [KeyboardButton(text="Alerts за 7")],
        [KeyboardButton(text="Alerts за 30 дней")],
        [KeyboardButton(text="Alerts за 90 дней")],
    ],
    resize_keyboard=True,   # кнопки подгоняются по ширине экрана
    one_time_keyboard=False # клавиатура не скрывается после нажатия
)

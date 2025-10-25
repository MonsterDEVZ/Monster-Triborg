"""
Модуль для создания Reply-клавиатур
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_standard_keyboard() -> ReplyKeyboardMarkup:
    """
    Стандартная Reply-клавиатура с двумя сервисными кнопками.
    Используется при старте бота и после завершения любых сценариев.

    Кнопки:
    - 🏠 Главное меню - возврат в начало
    - 🧑‍💻 Связаться с менеджером - прямая связь с живым менеджером

    Returns:
        ReplyKeyboardMarkup: Стандартная клавиатура
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Главное меню")],
            [KeyboardButton(text="🧑‍💻 Связаться с менеджером")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard


def get_contact_request_keyboard() -> ReplyKeyboardMarkup:
    """
    Временная Reply-клавиатура для запроса контакта пользователя.
    Используется в сценарии "Связь с менеджером" и при создании лидов.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопкой "Поделиться контактом"
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Поделиться контактом", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите кнопку ниже..."
    )
    return keyboard

"""
Обработчик команды /start с Deep Linking
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from packages.core.states.user_states import FunnelStates
from packages.core.utils.locales import locale_manager
from packages.core.keyboards import get_standard_keyboard

router = Router()


@router.message(CommandStart(deep_link=True))
async def handle_deeplink_start(
    message: Message, command: CommandObject, state: FSMContext, bot: Bot
):
    """
    Обработка /start с параметром (Deep Linking)
    Примеры: /start agency, /start cg, /start express
    """
    # Сбрасываем любое предыдущее состояние
    await state.clear()

    # Получаем payload из deep link
    payload = command.args

    # Проверяем, что payload соответствует одному из профилей
    valid_profiles = ["agency", "cg", "express"]
    if payload not in valid_profiles:
        # Если payload некорректный, показываем fallback
        await show_fallback_menu(message, state)
        return

    # Запускаем воронку для выбранного профиля
    await start_funnel(message, state, payload, bot)


@router.message(CommandStart(deep_link=False))
async def handle_plain_start(message: Message, state: FSMContext):
    """
    Обработка /start без параметров (Fallback сценарий)
    """
    # Сбрасываем любое предыдущее состояние
    await state.clear()

    # Показываем меню выбора направления
    await show_fallback_menu(message, state)


async def show_fallback_menu(message: Message, state: FSMContext):
    """
    Показать меню выбора направления (fallback)
    """
    fallback_data = locale_manager.get_fallback()

    # Создаём inline-клавиатуру из кнопок выбора направления
    buttons = []
    for button_data in fallback_data.get("buttons", []):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_data["text"], callback_data=button_data["callback_data"]
                )
            ]
        )

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    # Объединяем welcome text и "Выберите направление:" в одно сообщение
    combined_text = f"{fallback_data.get('welcome_text', '')}\n\nВыберите направление:"

    # ФАЗА 1: Отправляем приветственное сообщение СО СТАНДАРТНОЙ REPLY-КЛАВИАТУРОЙ
    # Это гарантирует, что кнопки [Главное меню] и [Связаться с менеджером]
    # появятся с самого первого взаимодействия
    await message.answer(
        combined_text,
        reply_markup=get_standard_keyboard()
    )

    # Отправляем inline-кнопки выбора направления отдельным сообщением
    await message.answer(
        "👇 Выберите направление:",
        reply_markup=inline_keyboard
    )

    # Устанавливаем состояние выбора направления
    await state.set_state(FunnelStates.choosing_direction)


async def start_funnel(message: Message, state: FSMContext, profile_name: str, bot: Bot):
    """
    Запустить воронку для выбранного профиля (Шаг 1)

    Args:
        message: Сообщение пользователя
        state: FSM Context
        profile_name: Название профиля (agency, cg, express)
        bot: Bot instance
    """
    # Получаем данные для Шага 1
    step1_data = locale_manager.get_step1_data(profile_name)

    # Создаём клавиатуру из кнопок
    buttons = []
    for button_data in step1_data.get("buttons", []):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_data["text"], callback_data=button_data["callback_data"]
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    # Получаем URL фото из конфига
    photo_url = step1_data.get("photo_url")
    caption = step1_data.get("caption", "")

    # Пытаемся отправить фото с inline-кнопками и Reply-клавиатурой одновременно
    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_url,
            caption=caption,
            reply_markup=keyboard,  # Inline-кнопки
        )
    except Exception as e:
        # Fallback: если фото не загрузилось, отправляем текстовое сообщение
        await message.answer(
            text=caption,
            reply_markup=keyboard,  # Inline-кнопки
        )

    # Сохраняем текущий профиль в состоянии
    await state.update_data(profile=profile_name, last_message_id=message.message_id)

    # Устанавливаем состояние Шага 1
    await state.set_state(FunnelStates.step1_qualification)

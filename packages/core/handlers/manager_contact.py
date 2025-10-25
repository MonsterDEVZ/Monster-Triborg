"""
Обработчик сценария "Связаться с менеджером"
Позволяет пользователю напрямую связаться с живым менеджером, минуя автоматическую воронку
"""
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from packages.core.keyboards import get_contact_request_keyboard, get_standard_keyboard
from packages.core.states.user_states import FunnelStates
from packages.core.utils.config import config

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "🧑‍💻 Связаться с менеджером")
async def handle_manager_contact_request(message: Message, state: FSMContext):
    """
    Обработчик нажатия на кнопку "Связаться с менеджером"
    Запрашивает контакт пользователя для прямой связи
    """
    username = message.from_user.username or "unknown"
    logger.info(f"🧑‍💻 User @{username} requested direct manager contact")

    # Сохраняем информацию о том, что это прямой запрос на связь с менеджером
    await state.update_data(
        direct_manager_contact=True,
        username=username
    )

    # Переводим в состояние ожидания контакта для сценария "Связь с менеджером"
    await state.set_state(FunnelStates.manager_contact_waiting)

    # Отправляем запрос контакта с временной клавиатурой
    await message.answer(
        "Понимаю! Чтобы я мог немедленно соединить вас с профильным менеджером, "
        "пожалуйста, поделитесь вашим контактом.",
        reply_markup=get_contact_request_keyboard()
    )

    logger.info(f"✅ Contact request sent to @{username} for manager contact scenario")


@router.message(FunnelStates.manager_contact_waiting, F.contact)
async def handle_manager_contact_received(message: Message, state: FSMContext, bot: Bot):
    """
    Обработчик получения контакта от пользователя в сценарии "Связь с менеджером"
    Отправляет приоритетное уведомление менеджеру и возвращает стандартную клавиатуру
    """
    # Получаем данные из состояния
    state_data = await state.get_data()
    username = state_data.get("username", message.from_user.username or "unknown")
    contact_name = message.from_user.full_name or "Telegram User"

    # Получаем телефон из контакта
    phone_number = message.contact.phone_number
    if not phone_number.startswith('+'):
        phone_number = f"+{phone_number}"

    logger.info(f"📞 Manager contact received from @{username}: {phone_number}")

    # Определяем текущий профиль (если есть)
    profile_name = state_data.get("profile", "НЕ УКАЗАН")
    profile_display_map = {
        "agency": "AGENCY",
        "cg": "CG",
        "express": "EXPRESS",
        "НЕ УКАЗАН": "НЕ УКАЗАН"
    }
    profile_display = profile_display_map.get(profile_name, profile_name.upper())

    # Формируем чистое деловое уведомление для менеджера
    urgent_notification = (
        f"<b>Срочный запрос на связь</b>\n\n"
        f"Клиент: @{username}\n"
        f"Телефон: {phone_number}\n"
        f"Имя: {contact_name}\n"
        f"Профиль: {profile_display}\n\n"
        f"Задача: Клиент ждет звонка/сообщения от менеджера."
    )

    # Отправляем уведомление в админ-чат
    try:
        await bot.send_message(
            chat_id=config.ADMIN_CHAT_ID,
            text=urgent_notification,
            parse_mode="HTML"
        )
        logger.info(f"✅ Urgent manager contact notification sent to admin for @{username}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления менеджеру: {e}", exc_info=True)

    # Отправляем подтверждение пользователю и возвращаем стандартную Reply-клавиатуру
    await message.answer(
        "✅ Спасибо! Ваша заявка передана. Менеджер свяжется с вами в Telegram "
        "или по телефону в течение 10-15 минут.",
        reply_markup=get_standard_keyboard()
    )

    # Очищаем состояние
    await state.clear()
    logger.info(f"✅ Manager contact scenario completed for @{username}, state cleared")


@router.message(F.text == "🏠 Главное меню")
async def handle_main_menu_button(message: Message, state: FSMContext):
    """
    Обработчик нажатия на кнопку "Главное меню"
    Возвращает пользователя в начало (эквивалент /start)
    """
    username = message.from_user.username or "unknown"
    logger.info(f"🏠 User @{username} requested main menu via Reply button")

    # Очищаем состояние
    await state.clear()

    # Импортируем обработчик старта
    from packages.core.handlers.start import handle_plain_start

    # Вызываем обработчик /start
    await handle_plain_start(message, state)

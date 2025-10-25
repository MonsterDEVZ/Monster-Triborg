"""
Обработчик follow-up сообщений (ссылки, ТЗ, дополнительная информация)
"""
import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from packages.core.states.user_states import FunnelStates
from packages.core.utils.locales import locale_manager
from packages.core.utils.config import config
from packages.core.keyboards import get_standard_keyboard

logger = logging.getLogger(__name__)

router = Router()


@router.message(FunnelStates.step4_waiting_followup)
async def handle_followup_message(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка follow-up сообщения от пользователя
    (ссылка на сайт, референсы, ТЗ и т.д.)

    Умное редактирование: Если есть admin_message_id, редактируем оригинальное сообщение.
    Иначе отправляем новое (для совместимости).
    """
    # Получаем данные из состояния
    state_data = await state.get_data()
    profile_name = state_data.get("profile")
    username = state_data.get("username", message.from_user.username or "unknown")
    admin_message_id = state_data.get("admin_message_id")
    last_choice = state_data.get("last_choice", "Запрос")
    phone_number = state_data.get("phone_number")  # НОВОЕ: получаем телефон

    if not profile_name:
        # Если профиль не найден, просто игнорируем
        return

    # Получаем данные профиля
    profile_data = locale_manager.get_profile(profile_name)
    brand_name = profile_data.get("name", "MONSTER")
    contact_name = message.from_user.full_name or "Telegram User"

    try:
        # СЦЕНАРИЙ 1: Если есть Message ID - редактируем оригинальное сообщение
        if admin_message_id:
            # Формируем обновленный текст с HTML форматированием
            updated_text = (
                f"✅ <b>ОБНОВЛЕНО: ССЫЛКА ПОЛУЧЕНА!</b>\n\n"
                f"⚠️ <b>[FALLBACK - CRM НЕДОСТУПНА]</b> ⚠️\n\n"
                f"🔥 <b>НОВЫЙ ЛИД: {brand_name}</b> 🔥\n\n"
                f"❗️ <i>Важно: Этот лид НЕ был создан в AmoCRM автоматически.\n"
                f"Требуется ручное внесение.</i>\n\n"
                f"<b>--- ДАННЫЕ ДЛЯ CRM ---</b>\n"
                f"<b>Запрос:</b> {last_choice}\n"
            )

            # Добавляем телефон, если есть
            if phone_number:
                updated_text += f"<b>Телефон:</b> {phone_number}\n"

            updated_text += (
                f"<b>Контакт:</b> @{username}\n"
                f"<b>Имя:</b> {contact_name}\n"
                f"<b>--------------------------</b>\n\n"
                f"📎 <b>FOLLOW-UP:</b>\n"
            )

            # Добавляем содержимое follow-up сообщения
            if message.text:
                updated_text += f"<b>Сообщение:</b> {message.text}\n"

            updated_text += (
                f"<b>--------------------------</b>\n\n"
                f"<b>Задача:</b>\n"
                f"1. Внести лид в AmoCRM вручную.\n"
                f"2. Связаться с клиентом в Telegram."
            )

            # Редактируем сообщение с HTML форматированием
            await bot.edit_message_text(
                chat_id=config.ADMIN_CHAT_ID,
                message_id=admin_message_id,
                text=updated_text,
                parse_mode="HTML"
            )

            logger.info(f"✅ Сообщение {admin_message_id} успешно отредактировано с follow-up данными")

            # Если есть медиафайлы, пересылаем их отдельно
            if message.document or message.photo or message.video:
                await bot.send_message(
                    chat_id=config.ADMIN_CHAT_ID,
                    text=f"📎 Дополнительные файлы от @{username}:"
                )
                await message.forward(chat_id=config.ADMIN_CHAT_ID)

        # СЦЕНАРИЙ 2: Если Message ID нет - отправляем новое сообщение (старая логика)
        else:
            followup_data = locale_manager.get_followup_data(profile_name)
            followup_template = followup_data.get("admin_followup_template", "")
            followup_text = followup_template.format(username=username, message=message.text)

            if message.text:
                await bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=followup_text)

            if message.document or message.photo or message.video:
                await bot.send_message(
                    chat_id=config.ADMIN_CHAT_ID,
                    text=f"📎 FOLLOW-UP от @{username} ({profile_name.upper()}):",
                )
                await message.forward(chat_id=config.ADMIN_CHAT_ID)

            logger.info(f"📤 Follow-up отправлен отдельным сообщением (нет admin_message_id)")

    except Exception as e:
        logger.error(f"❌ Ошибка обработки follow-up: {e}", exc_info=True)
        print(f"Ошибка отправки follow-up в админ-чат: {e}")

    # Подтверждаем получение и возвращаем стандартную Reply-клавиатуру
    await message.answer(
        "✅ Спасибо! Ваше дополнение отправлено менеджеру.",
        reply_markup=get_standard_keyboard()
    )

    # КРИТИЧЕСКИ ВАЖНО: Очищаем состояние, чтобы бот не "залипал"
    # После этого пользователь может начать новую воронку через /start
    await state.clear()

    logger.info(f"✅ Follow-up обработан, состояние очищено для @{username}")

"""
Обработчики callback-запросов (нажатий на кнопки)
"""
import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from packages.core.states.user_states import FunnelStates
from packages.core.utils.locales import locale_manager
from packages.core.utils.config import config
from packages.core.utils.crm import send_to_crm, build_crm_payload
from packages.core.handlers.start import start_funnel
from packages.core.keyboards import get_standard_keyboard

logger = logging.getLogger(__name__)

router = Router()


# === HELPER FUNCTIONS ===

async def finalize_and_send_lead(
    state: FSMContext,
    bot: Bot,
    profile_name: str,
    username: str,
    contact_name: str,
    phone_number: str,
    choice_text: str,
    golden_question_answer: str = "Клиент не ответил в течение 20 секунд"
):
    """
    Финальная функция для создания лида в CRM

    Эта функция вызывается из двух мест:
    1. Когда пользователь отвечает на золотой вопрос
    2. Когда истекает таймер (20 секунд)

    Args:
        state: FSM Context
        bot: Bot instance
        profile_name: Название профиля (agency, cg, express)
        username: Username пользователя
        contact_name: Имя контакта
        phone_number: Номер телефона
        choice_text: Выбранный вариант услуги
        golden_question_answer: Ответ на золотой вопрос или метка о таймауте
    """
    # Получаем профиль с webhook URL
    profile_data = locale_manager.get_profile(profile_name)
    brand_name = profile_data.get("name", "MONSTER")
    webhook_url = profile_data.get("webhook_url")

    # Отправляем лид в AmoCRM через вебхук
    if webhook_url:
        # Формируем payload для AmoCRM с номером телефона и ответом на золотой вопрос
        crm_payload = build_crm_payload(
            brand_name=brand_name,
            contact_name=contact_name,
            username=f"@{username}" if not username.startswith("id") else username,
            request_details=choice_text,
            phone=phone_number,
            additional_data={"golden_question_answer": golden_question_answer}
        )

        # Отправляем в AmoCRM
        crm_success = await send_to_crm(webhook_url, crm_payload)

        if not crm_success:
            # Если не удалось отправить в CRM, отправляем детальное fallback сообщение
            fallback_message = (
                f"⚠️ <b>[FALLBACK - CRM НЕДОСТУПНА]</b> ⚠️\n\n"
                f"🔥 <b>НОВЫЙ ЛИД: {brand_name}</b> 🔥\n\n"
                f"❗️ <i>Важно: Этот лид НЕ был создан в AmoCRM автоматически.\n"
                f"Требуется ручное внесение.</i>\n\n"
                f"<b>--- ДАННЫЕ ДЛЯ CRM ---</b>\n"
                f"<b>Запрос:</b> {choice_text}\n"
                f"<b>Телефон:</b> {phone_number}\n"
                f"<b>Контакт:</b> @{username}\n"
                f"<b>Имя:</b> {contact_name}\n"
                f"<b>Ответ на вопрос:</b> {golden_question_answer}\n"
                f"<b>--------------------------</b>\n\n"
                f"<b>Задача:</b>\n"
                f"1. Внести лид в AmoCRM вручную.\n"
                f"2. Связаться с клиентом по телефону или в Telegram."
            )
            try:
                await bot.send_message(
                    chat_id=config.ADMIN_CHAT_ID,
                    text=fallback_message,
                    parse_mode="HTML"
                )
                logger.warning(
                    f"⚠️ Fallback: Лид отправлен в Telegram для ручного внесения. "
                    f"Профиль: {profile_name}, Phone: {phone_number}, Username: @{username}"
                )
            except Exception as e:
                logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось отправить fallback в Telegram: {e}")
    else:
        # Если webhook не настроен, используем старую логику (Telegram)
        step2_data = locale_manager.get_step2_data(profile_name)
        admin_message = step2_data.get("admin_message_template", "").format(
            choice=choice_text, username=username
        )
        try:
            await bot.send_message(
                chat_id=config.ADMIN_CHAT_ID,
                text=f"⚠️ <b>[WEBHOOK НЕ НАСТРОЕН]</b>\n\n{admin_message}\n<b>Телефон:</b> {phone_number}\n<b>Ответ на вопрос:</b> {golden_question_answer}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Ошибка отправки в админ-чат: {e}")

    # Очищаем состояние
    await state.clear()
    logger.info(f"✅ Lead created in CRM and state cleared for @{username}")


# === CALLBACK HANDLERS ===

# УНИВЕРСАЛЬНЫЙ обработчик для ВСЕХ callback (без фильтра по состоянию)
# Он будет ловить нажатия на кнопки, даже если состояние не установлено
@router.callback_query(F.data.startswith("select_"))
async def handle_navigation_fallback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Универсальный обработчик для кнопок навигации (fallback menu)
    Срабатывает независимо от состояния FSM
    """
    callback_data = callback.data

    # Определяем профиль на основе callback_data
    profile_map = {
        "select_agency": "agency",
        "select_cg": "cg",
        "select_express": "express",
    }

    profile_name = profile_map.get(callback_data)
    if not profile_name:
        await callback.answer("Неизвестный выбор")
        return

    # Удаляем fallback-меню из чата для чистоты диалога
    try:
        await callback.message.delete()
        logger.info(f"🗑️ Fallback menu deleted for profile: {profile_name}")
    except Exception as e:
        logger.warning(f"⚠️ Не удалось удалить fallback-меню: {e}")
        # Если не удалось удалить, подтверждаем нажатие стандартным способом
        await callback.answer()

    logger.info(f"🔘 Fallback navigation: выбран профиль {profile_name}")

    # Запускаем воронку для выбранного профиля
    await start_funnel(callback.message, state, profile_name, bot)


@router.callback_query(FunnelStates.choosing_direction)
async def handle_direction_choice(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка выбора направления из fallback меню
    """
    callback_data = callback.data

    # Определяем профиль на основе callback_data
    profile_map = {
        "select_agency": "agency",
        "select_cg": "cg",
        "select_express": "express",
    }

    profile_name = profile_map.get(callback_data)
    if not profile_name:
        await callback.answer("Неизвестный выбор")
        return

    # Подтверждаем нажатие кнопки
    await callback.answer()

    # Запускаем воронку для выбранного профиля
    await start_funnel(callback.message, state, profile_name, bot)


# УНИВЕРСАЛЬНЫЙ обработчик для кнопок воронки (agency_*, cg_*, express_*)
# Срабатывает независимо от состояния FSM
@router.callback_query(
    F.data.startswith("agency_") |
    F.data.startswith("cg_") |
    F.data.startswith("express_")
)
async def handle_funnel_choice_fallback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Универсальный обработчик для кнопок воронки
    Срабатывает независимо от состояния FSM
    """
    callback_data = callback.data

    # Определяем профиль из callback_data
    if callback_data.startswith("agency_"):
        profile_name = "agency"
    elif callback_data.startswith("cg_"):
        profile_name = "cg"
    elif callback_data.startswith("express_"):
        profile_name = "express"
    else:
        await callback.answer("Неизвестный выбор")
        return

    # Получаем текст выбранной опции
    choice_text = locale_manager.get_choice_text(profile_name, callback_data)

    # Получаем username и имя пользователя
    username = callback.from_user.username or f"id{callback.from_user.id}"
    contact_name = callback.from_user.full_name or "Telegram User"

    # Подтверждаем нажатие кнопки (убираем "часики")
    await callback.answer("✅ Выбор принят!")

    logger.info(f"🔘 Funnel choice (fallback): профиль={profile_name}, выбор={choice_text}")

    # Редактируем предыдущее сообщение (с фото) - просим поделиться контактом
    contact_request_caption = (
        f"✅ Принято: {choice_text}.\n\n"
        f"👤 Для создания заявки поделитесь вашим контактом.\n\n"
        f"Нажмите кнопку ниже 👇"
    )

    try:
        # Редактируем caption (для фото), убираем inline-клавиатуру
        await callback.message.edit_caption(
            caption=contact_request_caption,
            reply_markup=None
        )
    except Exception:
        # Если сообщение не было с фото, редактируем текст
        try:
            await callback.message.edit_text(
                text=contact_request_caption,
                reply_markup=None
            )
        except Exception as e:
            logger.error(f"Ошибка редактирования сообщения: {e}")

    # Отправляем Reply-клавиатуру с кнопкой для запроса контакта
    contact_button = KeyboardButton(
        text="👤 Поделиться контактом",
        request_contact=True
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[contact_button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    # Сохраняем ID этого сообщения для последующего удаления
    contact_request_msg = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="📱 Нажмите кнопку для отправки контакта:",
        reply_markup=keyboard
    )

    # Сохраняем данные выбора для последующей отправки в CRM
    await state.update_data(
        profile=profile_name,
        username=username,
        contact_name=contact_name,
        last_choice=choice_text,
        contact_request_msg_id=contact_request_msg.message_id  # НОВОЕ: сохраняем ID
    )

    # Переводим в состояние ожидания контакта
    await state.set_state(FunnelStates.step2_waiting_contact)


@router.callback_query(FunnelStates.step1_qualification)
async def handle_step1_choice(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка выбора на Шаге 1 (квалификация)
    НОВАЯ ЛОГИКА: Запрашиваем контакт вместо немедленной отправки в CRM
    """
    # Получаем данные из состояния
    state_data = await state.get_data()
    profile_name = state_data.get("profile")

    if not profile_name:
        await callback.answer("Ошибка: профиль не найден")
        return

    # Получаем текст выбранной опции
    choice_text = locale_manager.get_choice_text(profile_name, callback.data)

    # Получаем username и имя пользователя
    username = callback.from_user.username or f"id{callback.from_user.id}"
    contact_name = callback.from_user.full_name or "Telegram User"

    # Редактируем предыдущее сообщение (с фото) - просим поделиться контактом
    contact_request_caption = (
        f"✅ Принято: {choice_text}.\n\n"
        f"👤 Для создания заявки поделитесь вашим контактом.\n\n"
        f"Нажмите кнопку ниже 👇"
    )

    try:
        # Редактируем caption (для фото), убираем inline-клавиатуру
        await callback.message.edit_caption(
            caption=contact_request_caption,
            reply_markup=None
        )
    except Exception:
        # Если сообщение не было с фото, редактируем текст
        try:
            await callback.message.edit_text(
                text=contact_request_caption,
                reply_markup=None
            )
        except Exception as e:
            print(f"Ошибка редактирования сообщения: {e}")

    # Подтверждаем нажатие кнопки
    await callback.answer("✅ Выбор принят!")

    # Отправляем Reply-клавиатуру с кнопкой для запроса контакта
    contact_button = KeyboardButton(
        text="👤 Поделиться контактом",
        request_contact=True
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[contact_button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    # Сохраняем ID этого сообщения для последующего удаления
    contact_request_msg = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="📱 Нажмите кнопку для отправки контакта:",
        reply_markup=keyboard
    )

    # Сохраняем данные выбора для последующей отправки в CRM
    await state.update_data(
        profile=profile_name,
        username=username,
        contact_name=contact_name,
        last_choice=choice_text,
        contact_request_msg_id=contact_request_msg.message_id  # НОВОЕ: сохраняем ID
    )

    # Переводим в состояние ожидания контакта
    await state.set_state(FunnelStates.step2_waiting_contact)


@router.message(FunnelStates.step2_waiting_contact, F.text)
async def handle_invalid_contact_input(message: Message, state: FSMContext):
    """
    Валидация: Обработка неправильного ввода (текст вместо контакта)
    Действия:
    1. Удаляем сообщение пользователя
    2. Отправляем подсказку
    3. Не меняем состояние FSM (остаемся на шаге ожидания контакта)
    """
    username = message.from_user.username or f"id{message.from_user.id}"
    logger.warning(f"⚠️ User @{username} sent text instead of contact: {message.text}")

    # Удаляем неправильное сообщение пользователя
    try:
        await message.delete()
        logger.info(f"🗑️ Deleted invalid text message from @{username}")
    except Exception as e:
        logger.warning(f"⚠️ Не удалось удалить сообщение пользователя: {e}")

    # Отправляем подсказку
    await message.answer(
        "Пожалуйста, используйте кнопку '👤 Поделиться контактом' ниже. "
        "Это самый быстрый и безопасный способ."
    )

    logger.info(f"✅ Validation reminder sent to @{username}, staying in contact waiting state")


@router.message(FunnelStates.step2_waiting_contact, F.contact)
async def handle_contact_received(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка получения контакта (номера телефона)
    НОВАЯ ЛОГИКА (REFACTORED):
    1. Удаляем сообщение с просьбой нажать кнопку
    2. Отправляем лид в CRM немедленно
    3. Задаем финальный вопрос про сайт/Instagram
    4. Переходим в состояние ожидания follow-up

    "Золотой вопрос" удален. Отправка в CRM происходит СРАЗУ после получения контакта.
    """
    # Извлекаем данные контакта
    contact = message.contact
    phone_number = contact.phone_number
    if not phone_number.startswith('+'):
        phone_number = f"+{phone_number}"
    contact_first_name = contact.first_name or ""

    # Получаем сохраненные данные из состояния
    state_data = await state.get_data()
    profile_name = state_data.get("profile")
    username = state_data.get("username", f"id{message.from_user.id}")
    contact_name = state_data.get("contact_name", contact_first_name)
    choice_text = state_data.get("last_choice", "")
    contact_request_msg_id = state_data.get("contact_request_msg_id")

    if not profile_name:
        await message.answer("Ошибка: профиль не найден", reply_markup=get_standard_keyboard())
        return

    logger.info(f"📞 Contact received from @{username}: {phone_number}")

    # ФАЗА 1: Удаляем сообщение "📱 Нажмите кнопку для отправки контакта:"
    if contact_request_msg_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=contact_request_msg_id
            )
            logger.info(f"🗑️ Deleted contact request message (ID: {contact_request_msg_id})")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось удалить сообщение с кнопкой: {e}")

    # ФАЗА 2: ОТПРАВЛЯЕМ ЛИД В CRM НЕМЕДЛЕННО
    profile_data = locale_manager.get_profile(profile_name)
    brand_name = profile_data.get("name", "MONSTER")
    webhook_url = profile_data.get("webhook_url")

    if webhook_url:
        # Формируем payload для AmoCRM
        crm_payload = build_crm_payload(
            brand_name=brand_name,
            contact_name=contact_name,
            username=f"@{username}" if not username.startswith("id") else username,
            request_details=choice_text,
            phone=phone_number
        )

        # Отправляем в AmoCRM
        crm_success = await send_to_crm(webhook_url, crm_payload)

        if crm_success:
            logger.info(f"✅ Lead sent to CRM successfully for @{username}")
        else:
            # Fallback: отправляем в админ-чат
            logger.warning(f"❌ CRM webhook failed for @{username}, sending fallback notification")

            profile_display_map = {
                "agency": "AGENCY",
                "cg": "CG",
                "express": "EXPRESS"
            }
            profile_display = profile_display_map.get(profile_name, profile_name.upper())

            fallback_message = (
                f"⚠️ <b>[FALLBACK - CRM НЕДОСТУПНА]</b> ⚠️\n\n"
                f"🔥 <b>НОВЫЙ ЛИД: {brand_name}</b> 🔥\n\n"
                f"❗️ <i>Важно: Этот лид НЕ был создан в AmoCRM автоматически.\\n"
                f"Требуется ручное внесение.</i>\n\n"
                f"<b>--- ДАННЫЕ ДЛЯ CRM ---</b>\n"
                f"<b>Запрос:</b> {choice_text}\n"
                f"<b>Телефон:</b> {phone_number}\n"
                f"<b>Контакт:</b> @{username}\n"
                f"<b>Имя:</b> {contact_name}\n"
                f"<b>--------------------------</b>\n\n"
                f"<b>Задача:</b> Внести лид в AmoCRM вручную и связаться в Telegram."
            )

            await bot.send_message(
                chat_id=config.ADMIN_CHAT_ID,
                text=fallback_message,
                parse_mode="HTML"
            )

    # ШАГ 2: "ЖЕЛЕЗОБЕТОННЫЙ" ВОЗВРАТ КЛАВИАТУРЫ
    # Отправляем подтверждение, к которому ПРИНУДИТЕЛЬНО прикреплена стандартная клавиатура.
    # Это говорит Telegram: "Забудь про все, что было раньше. Прямо сейчас покажи вот эту клавиатуру".
    await message.answer(
        text="✅ Спасибо! Заявка принята.",
        reply_markup=get_standard_keyboard()
    )
    logger.info(f"✅ Standard keyboard returned for @{username}")

    # ШАГ 3: Задаем финальный вопрос про сайт/Instagram
    # Это сообщение идет уже ПОСЛЕ возврата клавиатуры
    final_question_data = profile_data.get("final_question", {})
    final_question_text = final_question_data.get("text", "")

    if final_question_text:
        await message.answer(
            text="💡 Чтобы мы подготовились лучше, пришлите ссылку на ваш сайт или Instagram."
        )

        # ШАГ 4: Сохраняем данные для отслеживания follow-up
        await state.update_data(
            profile=profile_name,
            username=username,
            contact_name=contact_name,
            phone_number=phone_number,
            last_choice=choice_text,
        )

        # Переводим в состояние ожидания follow-up (ссылки на сайт/Instagram)
        await state.set_state(FunnelStates.step4_waiting_followup)

        logger.info(f"✅ Final question sent to @{username}, waiting for follow-up")
    else:
        # Если финального вопроса нет, просто завершаем воронку
        await state.clear()
        logger.info(f"✅ Funnel completed for @{username}, no final question configured")

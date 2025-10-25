"""
Временный скрипт для получения Chat ID
Запустите этот скрипт и напишите боту любое сообщение
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from packages.core.utils.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
@router.message(F.text)
async def get_chat_id_handler(message: Message):
    """Обработчик для получения Chat ID"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or "нет username"
    first_name = message.from_user.first_name or ""

    response = (
        f"✅ <b>Информация о вашем аккаунте:</b>\n\n"
        f"👤 Имя: {first_name}\n"
        f"🆔 Username: @{username}\n"
        f"📋 User ID: <code>{user_id}</code>\n"
        f"💬 Chat ID: <code>{chat_id}</code>\n\n"
        f"<b>Для бота используйте:</b>\n"
        f"<code>ADMIN_CHAT_ID={chat_id}</code>\n\n"
        f"📝 Скопируйте число <code>{chat_id}</code> и добавьте в .env файл"
    )

    await message.answer(response, parse_mode="HTML")

    logger.info(f"📋 Chat ID для .env: {chat_id}")
    logger.info(f"👤 Пользователь: {first_name} (@{username})")


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("🤖 Бот запущен!")
    logger.info("📱 Откройте бота в Telegram и отправьте /start или любое сообщение")
    logger.info("📋 Вы получите ваш Chat ID")
    logger.info("⏹️  Для остановки нажмите Ctrl+C")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")

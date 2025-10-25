"""
Главная точка входа для Monster Triborg Bot
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Импортируем конфигурацию
from packages.core.utils.config import config

# Импортируем роутеры
from packages.core.handlers import start, callbacks, followup, manager_contact

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""

    # Инициализация бота и диспетчера
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Используем MemoryStorage для MVP (в production можно заменить на Redis)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры в правильном порядке
    dp.include_router(start.router)  # Обработчики /start
    dp.include_router(manager_contact.router)  # Обработчики "Связь с менеджером"
    dp.include_router(callbacks.router)  # Обработчики callback-запросов
    dp.include_router(followup.router)  # Обработчики follow-up сообщений

    logger.info("🚀 Monster Triborg Bot запущен!")
    logger.info(f"📋 Admin Chat ID: {config.ADMIN_CHAT_ID}")

    try:
        # Удаляем webhook (если был установлен)
        await bot.delete_webhook(drop_pending_updates=True)

        # Запускаем polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("❌ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)

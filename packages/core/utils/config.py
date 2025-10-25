"""
Конфигурация бота и загрузка переменных окружения
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из корня проекта
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Конфигурация бота"""

    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не установлен в .env файле")

    # Admin Chat ID для отправки заявок
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
    if not ADMIN_CHAT_ID:
        raise ValueError("ADMIN_CHAT_ID не установлен в .env файле")

    # Опционально: Redis для production
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    # Путь к файлу локализации
    LOCALES_PATH = project_root / "locales" / "locales.json"


# Экземпляр конфигурации
config = Config()

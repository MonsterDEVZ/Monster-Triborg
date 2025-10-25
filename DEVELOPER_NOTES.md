# 👨‍💻 Заметки для разработчиков

## 🔍 Важные детали реализации

### 1. Почему `answer()` вместо `answer_photo()` в start.py?

В `packages/core/handlers/start.py:105` используется:
```python
await message.answer(
    f"🖼 [Фото: {photo_id}]\n\n{step1_data.get('caption', '')}",
    reply_markup=keyboard,
)
```

**Это сделано намеренно** для быстрого MVP без реальных фото.

**Для production замените на:**
```python
await message.answer_photo(
    photo=step1_data.get("photo_id"),  # Реальный file_id
    caption=step1_data.get('caption', ''),
    reply_markup=keyboard,
)
```

**Как получить file_id:**
1. Отправьте фото вашему боту
2. Добавьте временный обработчик:
```python
@router.message(F.photo)
async def get_photo_id(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f"file_id: {photo_id}")
```
3. Скопируйте file_id в `locales.json`

---

### 2. Редактирование сообщений в callbacks.py

В `packages/core/handlers/callbacks.py:48` есть try/except для редактирования:

```python
try:
    await callback.message.edit_caption(...)
except:
    await callback.message.edit_text(...)
```

**Почему так?**
- Если Шаг 1 был с фото → используем `edit_caption()`
- Если Шаг 1 был с текстом → используем `edit_text()`

**В production с реальными фото** оставьте только:
```python
await callback.message.edit_caption(
    caption=success_caption,
    reply_markup=None
)
```

---

### 3. FSM States: когда сбрасывать?

**Сбрасываем состояние (`state.clear()`):**
- При новом запуске `/start` (чтобы начать с чистого листа)
- При переходе по deep link (новый контекст)

**НЕ сбрасываем:**
- После отправки заявки (для follow-up)
- Во время ожидания дополнительной информации

**Пример в start.py:**
```python
@router.message(CommandStart(deep_link=True))
async def handle_deeplink_start(...):
    await state.clear()  # ✅ Сброс при новом deep link
```

---

### 4. Обработка пользователей без username

В `callbacks.py:26`:
```python
username = callback.from_user.username or "unknown"
```

**Проблема:** ~10% пользователей Telegram не имеют @username

**Решение:**
```python
# Текущее (базовое):
username = callback.from_user.username or "unknown"

# Улучшенное:
username = callback.from_user.username or f"id{callback.from_user.id}"

# С именем:
if callback.from_user.username:
    contact = f"@{callback.from_user.username}"
else:
    name = callback.from_user.full_name or "Пользователь"
    contact = f"{name} (ID: {callback.from_user.id})"
```

---

### 5. Множественные follow-up сообщения

В `followup.py:42` состояние **не сбрасывается** после follow-up:

```python
# Оставляем состояние как есть
# await state.clear()  ← НЕ делаем этого
```

**Почему?**
- Пользователь может отправить несколько сообщений
- Все будут переданы в админ-чат
- Удобно для клиента (не нужно начинать заново)

**Если нужно ограничить до одного follow-up:**
```python
await message.answer("✅ Спасибо! ...")
await state.clear()  # ✅ Сбросить после первого
```

---

## 🐛 Типичные ошибки и решения

### Ошибка 1: `ModuleNotFoundError: No module named 'packages'`

**Причина:** Python не может найти модуль `packages`

**Решение 1:** Запускайте из корня проекта:
```bash
cd /Users/new/Desktop/Проекты/Monster/Monster-Triborg
python3 apps/bot/main.py
```

**Решение 2:** Добавьте корень в PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/Monster-Triborg"
```

**Решение 3:** В `apps/bot/main.py` добавьте:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

---

### Ошибка 2: `ValueError: BOT_TOKEN не установлен`

**Причина:** Файл `.env` не найден или пуст

**Решение:**
```bash
# Проверьте, что .env существует
ls -la .env

# Проверьте содержимое
cat .env

# Создайте, если нет
cp .env.example .env

# Отредактируйте
nano .env
```

---

### Ошибка 3: Бот не отвечает на сообщения

**Возможные причины:**
1. Неверный токен
2. Бот не запущен
3. Состояние FSM блокирует обработчик

**Диагностика:**
```python
# Добавьте в main.py для отладки:
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Проверка токена:**
```bash
curl https://api.telegram.org/bot<ВАШ_ТОКЕН>/getMe
```

---

### Ошибка 4: Заявки не приходят в админ-чат

**Проверьте:**
1. ADMIN_CHAT_ID корректный?
```bash
echo $ADMIN_CHAT_ID
```

2. Для групповых чатов ID начинается с `-`
```
ADMIN_CHAT_ID=-1001234567890
```

3. Бот добавлен в групповой чат?

**Получить Chat ID группы:**
1. Добавьте бота в группу
2. Отправьте любое сообщение
3. Откройте: `https://api.telegram.org/bot<ТОКЕН>/getUpdates`
4. Найдите `"chat":{"id":-1001234567890,...}`

---

## 🔧 Расширение функциональности

### Добавление нового профиля

**Шаг 1:** Добавьте в `locales/locales.json`:
```json
{
  "custom": {
    "name": "CUSTOM PROFILE",
    "step1": {
      "photo_id": "custom_step1_photo",
      "caption": "Ваш вопрос?",
      "buttons": [
        {"text": "Вариант 1", "callback_data": "custom_opt1"},
        {"text": "Вариант 2", "callback_data": "custom_opt2"}
      ]
    },
    "step2": {
      "success_caption_template": "Принято: {choice}...",
      "admin_message_template": "🔥 НОВЫЙ ЛИД: CUSTOM\n\n...",
      "choices": {
        "custom_opt1": "Вариант 1",
        "custom_opt2": "Вариант 2"
      }
    },
    "followup": {
      "admin_followup_template": "📎 FOLLOW-UP от @{username} (CUSTOM):\n\n{message}"
    }
  }
}
```

**Шаг 2:** Добавьте в fallback кнопку:
```json
{
  "fallback": {
    "buttons": [
      ...
      {"text": "🎯 Custom", "callback_data": "select_custom"}
    ]
  }
}
```

**Шаг 3:** Обновите `callbacks.py`:
```python
profile_map = {
    "select_agency": "agency",
    "select_cg": "cg",
    "select_express": "express",
    "select_custom": "custom",  # ✅ Добавьте
}
```

**Готово!** Deep link: `t.me/bot?start=custom`

---

### Добавление логирования в файл

В `apps/bot/main.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

# Создайте директорию для логов
Path("logs").mkdir(exist_ok=True)

# Настройте логирование
handler = RotatingFileHandler(
    "logs/bot.log",
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

### Добавление метрик и аналитики

Создайте `packages/core/utils/analytics.py`:
```python
import logging
from datetime import datetime

analytics_logger = logging.getLogger("analytics")

def log_lead(profile: str, choice: str, username: str):
    """Логирование лида для аналитики"""
    analytics_logger.info(
        f"LEAD | {datetime.now().isoformat()} | "
        f"{profile} | {choice} | @{username}"
    )

def log_followup(profile: str, username: str):
    """Логирование follow-up"""
    analytics_logger.info(
        f"FOLLOWUP | {datetime.now().isoformat()} | "
        f"{profile} | @{username}"
    )
```

Используйте в `callbacks.py`:
```python
from packages.core.utils.analytics import log_lead

# После отправки в админ-чат:
log_lead(profile_name, choice_text, username)
```

---

### Интеграция с AmoCRM

Создайте `packages/core/utils/crm.py`:
```python
import aiohttp
from packages.core.utils.config import config

async def send_to_amocrm(username: str, choice: str, profile: str):
    """Отправка лида в AmoCRM"""
    url = f"https://{config.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads"

    headers = {
        "Authorization": f"Bearer {config.AMOCRM_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "name": f"Лид из Telegram: {profile}",
        "price": 0,
        "custom_fields_values": [
            {
                "field_id": 123,  # ID поля "Telegram"
                "values": [{"value": f"@{username}"}]
            },
            {
                "field_id": 456,  # ID поля "Запрос"
                "values": [{"value": choice}]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=[data]) as resp:
            if resp.status != 200:
                print(f"Ошибка AmoCRM: {await resp.text()}")
```

Используйте в `callbacks.py`:
```python
from packages.core.utils.crm import send_to_amocrm

# После отправки в админ-чат:
await send_to_amocrm(username, choice_text, profile_name)
```

---

## 🎨 Кастомизация для клиентов

### Изменение эмодзи и стиля

В `locales.json` можно изменить эмодзи для брендинга:
```json
{
  "agency": {
    "step1": {
      "buttons": [
        {"text": "🚀 Запустить рост", "callback_data": "agency_attract"}
      ]
    }
  }
}
```

### Добавление дополнительных вопросов

Расширьте FSM в `user_states.py`:
```python
class FunnelStates(StatesGroup):
    choosing_direction = State()
    step1_qualification = State()
    step1_5_additional = State()  # ✅ Новое состояние
    step2_waiting_followup = State()
```

Добавьте обработчик между Шагом 1 и 2.

---

## 📊 Production Checklist

### Перед деплоем:

- [ ] Замените `answer()` на `answer_photo()` с реальными file_id
- [ ] Настройте Redis вместо MemoryStorage
- [ ] Добавьте логирование в файл
- [ ] Настройте мониторинг (например, Sentry)
- [ ] Добавьте graceful shutdown
- [ ] Настройте systemd/supervisor для автозапуска
- [ ] Настройте backup для .env
- [ ] Добавьте rate limiting (защита от спама)
- [ ] Протестируйте все сценарии
- [ ] Настройте алерты в админ-чат при ошибках

### Graceful Shutdown:

В `main.py`:
```python
import signal

async def shutdown(dp: Dispatcher, bot: Bot):
    logger.info("Shutting down...")
    await dp.storage.close()
    await bot.session.close()

async def main():
    # ...

    # Обработка сигналов
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(shutdown(dp, bot))
        )

    await dp.start_polling(bot)
```

---

## 📚 Полезные ссылки

- [Документация aiogram 3.x](https://docs.aiogram.dev/en/latest/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Deep Linking в Telegram](https://core.telegram.org/bots/features#deep-linking)
- [FSM в aiogram](https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/index.html)

---

**Удачи в разработке! 🚀**

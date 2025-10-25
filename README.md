# Monster Triborg Bot 🤖

Интеллектуальный Telegram-бот-маршрутизатор для **Monster Agency**, **Monster CG** и **Monster Express**.

## 🎯 Основные возможности

- **Deep Linking**: Мгновенная адаптация под контекст клиента через параметры `/start`
- **Сверхбыстрые воронки**: 2 шага до заявки
- **Умная маршрутизация**: Автоматическое определение направления бизнеса
- **Follow-up система**: Сбор дополнительной информации (ссылки, ТЗ, референсы)
- **Единая архитектура**: Core + Apps для масштабируемости

## 🏗️ Архитектура

```
Monster-Triborg/
├── packages/core/              # Бизнес-логика (ядро)
│   ├── handlers/              # Обработчики событий
│   │   ├── start.py          # Deep Linking + Fallback
│   │   ├── callbacks.py      # Обработка кнопок
│   │   └── followup.py       # Follow-up сообщения
│   ├── states/               # FSM States
│   │   └── user_states.py
│   └── utils/                # Утилиты
│       ├── config.py         # Конфигурация
│       └── locales.py        # Локализация
├── apps/bot/                  # Точка входа
│   └── main.py               # Запуск бота
├── locales/                   # Контент
│   └── locales.json          # Тексты всех воронок
├── .env.example              # Шаблон конфигурации
└── requirements.txt          # Зависимости
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка конфигурации

```bash
# Скопируйте шаблон .env
cp .env.example .env

# Отредактируйте .env и добавьте:
# BOT_TOKEN=ваш_токен_бота
# ADMIN_CHAT_ID=ваш_chat_id
```

**Как получить токен бота?**
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot` и следуйте инструкциям
3. Скопируйте токен в `.env`

**Как узнать ADMIN_CHAT_ID?**
1. Напишите [@userinfobot](https://t.me/userinfobot)
2. Скопируйте ваш ID в `.env`

### 3. Настройка фото для воронок

В файле `locales/locales.json` замените placeholder'ы на реальные file_id фотографий:

```json
{
  "agency": {
    "step1": {
      "photo_id": "AgACAgIAAxkBAAI..."  // Замените на реальный file_id
    }
  }
}
```

**Как получить file_id фото?**
1. Отправьте фото боту [@userinfobot](https://t.me/userinfobot)
2. Скопируйте `file_id` из ответа
3. Вставьте в `locales.json`

Или временно используйте текстовые заглушки (как сейчас).

### 4. Запуск бота

```bash
# Из корня проекта
python3 apps/bot/main.py
```

Вы увидите:
```
🚀 Monster Triborg Bot запущен!
📋 Admin Chat ID: 123456789
```

## 🔗 Deep Linking

### Прямые ссылки для каждого направления:

- **Monster Agency**: `https://t.me/ВАШ_БОТ?start=agency`
- **Monster CG**: `https://t.me/ВАШ_БОТ?start=cg`
- **Monster Express**: `https://t.me/ВАШ_БОТ?start=express`

### Fallback (без параметра):
- `https://t.me/ВАШ_БОТ` — покажет меню выбора направления

## 📊 Сценарии работы

### Профиль 1: Monster Agency (`start=agency`)

**Шаг 1: Визуальная Квалификация**
- Показывается фото с кнопками:
  - 📈 Привлечь клиентов
  - 💰 Увеличить продажи
  - 🎯 Улучшить рекламу

**Шаг 2: Завершение и обогащение**
- Автоматически получается @username
- Заявка мгновенно отправляется в админ-чат
- Бот просит ссылку на сайт/соцсети

### Профиль 2: Monster CG (`start=cg`)

**Шаг 1: Визуальная Квалификация**
- 🤖 AI-видео
- ✨ Спецэффекты (VFX)
- 🧊 Компьютерная графика (CG)

**Шаг 2: Завершение**
- Заявка в админ-чат
- Бот просит референсы

### Профиль 3: Monster Express (`start=express`)

**Шаг 1: Визуальная Квалификация**
- 💻 Сайт / Лендинг
- 🎬 Баннер-анимация
- ✨ AI-видео

**Шаг 2: Завершение**
- Заявка в админ-чат
- Бот просит ТЗ (в течение 15 минут)

## 🔧 Технологический стек

- **Python 3.10+**
- **aiogram 3.13.1** — асинхронная работа с Telegram Bot API
- **python-dotenv** — управление конфигурацией
- **MemoryStorage** — FSM хранилище (для MVP)
- **black** — форматирование кода

## 📝 Редактирование контента

Все тексты, кнопки и настройки находятся в `locales/locales.json`. Вы можете легко изменять:
- Тексты сообщений
- Названия кнопок
- Шаблоны уведомлений
- ID фотографий

Пример:
```json
{
  "agency": {
    "step1": {
      "caption": "Ваш новый текст здесь",
      "buttons": [
        {
          "text": "🔥 Новая кнопка",
          "callback_data": "agency_new"
        }
      ]
    }
  }
}
```

## 🎨 Форматирование кода

```bash
# Форматирование всех файлов
black .

# Проверка без изменений
black --check .
```

## 🚀 Деплой на Production

### Вариант 1: VPS/Dedicated Server

```bash
# Установите supervisor для автозапуска
sudo apt install supervisor

# Создайте конфигурацию
sudo nano /etc/supervisor/conf.d/monster-bot.conf
```

```ini
[program:monster-bot]
directory=/path/to/Monster-Triborg
command=/path/to/venv/bin/python apps/bot/main.py
user=youruser
autostart=true
autorestart=true
stderr_logfile=/var/log/monster-bot.err.log
stdout_logfile=/var/log/monster-bot.out.log
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start monster-bot
```

### Вариант 2: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "apps/bot/main.py"]
```

```bash
docker build -t monster-bot .
docker run -d --env-file .env monster-bot
```

### Для Production: Замените MemoryStorage на Redis

В `apps/bot/main.py`:

```python
from aiogram.fsm.storage.redis import RedisStorage
storage = RedisStorage.from_url("redis://localhost:6379/0")
```

## 🐛 Troubleshooting

**Бот не отвечает:**
- Проверьте `BOT_TOKEN` в `.env`
- Убедитесь, что бот запущен (`python3 apps/bot/main.py`)

**Заявки не приходят в админ-чат:**
- Проверьте `ADMIN_CHAT_ID` в `.env`
- Убедитесь, что бот добавлен в чат (для групповых чатов)

**Фото не отображаются:**
- Замените `photo_id` в `locales.json` на реальные file_id

## 📄 Лицензия

MIT License - используйте свободно для любых целей.

## 👨‍💻 Автор

Created with ❤️ for Monster Corp by Claude Code

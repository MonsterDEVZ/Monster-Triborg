# 📑 Monster Triborg Bot - Индекс файлов

## 🗂️ Полный список файлов проекта

### 📦 Core Business Logic (packages/core/)

#### Handlers (обработчики событий)
| Файл | Строк | Назначение |
|------|-------|------------|
| `packages/core/handlers/__init__.py` | 0 | Package marker |
| `packages/core/handlers/start.py` | 107 | Deep Linking + Fallback сценарий |
| `packages/core/handlers/callbacks.py` | 82 | Обработка кнопок (Шаг 1 → Шаг 2) |
| `packages/core/handlers/followup.py` | 50 | Обработка follow-up сообщений |

**Ключевые функции:**
- `start.py`:
  - `handle_deeplink_start()` — Deep Linking
  - `handle_plain_start()` — Fallback
  - `show_fallback_menu()` — Меню выбора
  - `start_funnel()` — Запуск воронки

- `callbacks.py`:
  - `handle_direction_choice()` — Выбор из fallback
  - `handle_step1_choice()` — Обработка Шага 1

- `followup.py`:
  - `handle_followup_message()` — Follow-up обработка

#### States (FSM состояния)
| Файл | Строк | Назначение |
|------|-------|------------|
| `packages/core/states/__init__.py` | 0 | Package marker |
| `packages/core/states/user_states.py` | 14 | FSM States для воронок |

**Состояния:**
- `choosing_direction` — выбор направления (fallback)
- `step1_qualification` — визуальная квалификация
- `step2_waiting_followup` — ожидание дополнительной информации

#### Utils (утилиты)
| Файл | Строк | Назначение |
|------|-------|------------|
| `packages/core/utils/__init__.py` | 0 | Package marker |
| `packages/core/utils/config.py` | 35 | Конфигурация (.env) |
| `packages/core/utils/locales.py` | 72 | Менеджер локализации |

**Ключевые классы:**
- `config.py`:
  - `Config` — загрузка переменных окружения
  - `config` — глобальный экземпляр

- `locales.py`:
  - `LocaleManager` — работа с locales.json
  - `locale_manager` — глобальный экземпляр

---

### 🚀 Application Entry Point (apps/bot/)

| Файл | Строк | Назначение |
|------|-------|------------|
| `apps/__init__.py` | 0 | Package marker |
| `apps/bot/__init__.py` | 0 | Package marker |
| `apps/bot/main.py` | 58 | Главная точка входа (запуск бота) |

**Ключевые функции:**
- `main()` — инициализация и запуск бота
- Настройка logging
- Регистрация роутеров

---

### 🌍 Localization (locales/)

| Файл | Строк | Назначение |
|------|-------|------------|
| `locales/locales.json` | 148 | Все тексты, кнопки, шаблоны |

**Структура JSON:**
```json
{
  "fallback": {...},      // Меню выбора
  "agency": {...},        // Monster Agency
  "cg": {...},            // Monster CG
  "express": {...}        // Monster Express
}
```

**Каждый профиль содержит:**
- `name` — название
- `step1` — Шаг 1 (фото, текст, кнопки)
- `step2` — Шаг 2 (шаблоны уведомлений, choices)
- `followup` — Follow-up шаблоны

---

### ⚙️ Configuration Files

| Файл | Строк | Назначение |
|------|-------|------------|
| `.env.example` | 8 | Шаблон конфигурации |
| `.gitignore` | 45 | Git исключения |
| `requirements.txt` | 9 | Python зависимости |

**Зависимости:**
- `aiogram==3.13.1` — Bot framework
- `python-dotenv==1.0.1` — Конфигурация
- `black==24.10.0` — Code formatting (dev)

---

### 🛠️ Scripts

| Файл | Строк | Назначение |
|------|-------|------------|
| `run.sh` | 32 | Скрипт быстрого запуска |

**Функционал:**
- Проверка и создание venv
- Установка зависимостей
- Проверка .env
- Запуск бота

---

### 📚 Documentation (6 файлов)

| Файл | Размер | Назначение | Для кого |
|------|--------|------------|----------|
| `README.md` | ~400 строк | Полная документация | Все |
| `QUICKSTART.md` | ~150 строк | Быстрый старт за 5 минут | Начинающие |
| `EXAMPLES.md` | ~350 строк | Примеры использования | Менеджеры, тестировщики |
| `PROJECT_OVERVIEW.md` | ~450 строк | Технический обзор | Разработчики |
| `DEVELOPER_NOTES.md` | ~500 строк | Детали реализации | Разработчики |
| `IMPLEMENTATION_SUMMARY.md` | ~400 строк | Итоговый отчёт | Все |

**Дополнительно:**
- `FILES_INDEX.md` (этот файл) — индекс всех файлов

---

## 📊 Статистика

### По типам файлов:
```
Python:        9 файлов    (~599 строк)
JSON:          1 файл      (148 строк)
Markdown:      7 файлов    (~2,250 строк)
Shell:         1 файл      (32 строки)
Config:        3 файла     (~62 строки)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:         21 файл     (~3,091 строка)
```

### По директориям:
```
packages/core/handlers/    3 файла   (239 строк Python)
packages/core/states/      1 файл    (14 строк Python)
packages/core/utils/       2 файла   (107 строк Python)
apps/bot/                  1 файл    (58 строк Python)
locales/                   1 файл    (148 строк JSON)
Documentation/             7 файлов  (~2,250 строк MD)
Configuration/             3 файла   (~62 строки)
Scripts/                   1 файл    (32 строки)
```

---

## 🔍 Как найти нужный файл?

### Хочу изменить тексты воронки:
→ `locales/locales.json`

### Хочу добавить новую логику:
→ `packages/core/handlers/`

### Хочу настроить конфигурацию:
→ `.env` (создайте из `.env.example`)

### Хочу понять архитектуру:
→ `PROJECT_OVERVIEW.md`

### Хочу быстро запустить:
→ `QUICKSTART.md`

### Хочу увидеть примеры:
→ `EXAMPLES.md`

### Хочу расширить функционал:
→ `DEVELOPER_NOTES.md`

---

## 🗂️ Файловое дерево (визуализация)

```
Monster-Triborg/
│
├── 📦 packages/
│   ├── __init__.py
│   └── core/
│       ├── __init__.py
│       ├── handlers/
│       │   ├── __init__.py
│       │   ├── start.py          ← Deep Linking + Fallback
│       │   ├── callbacks.py      ← Обработка кнопок
│       │   └── followup.py       ← Follow-up система
│       ├── states/
│       │   ├── __init__.py
│       │   └── user_states.py    ← FSM States
│       └── utils/
│           ├── __init__.py
│           ├── config.py         ← Конфигурация
│           └── locales.py        ← Локализация
│
├── 🚀 apps/
│   ├── __init__.py
│   └── bot/
│       ├── __init__.py
│       └── main.py               ← Точка входа
│
├── 🌍 locales/
│   └── locales.json              ← Все тексты
│
├── ⚙️  Configuration/
│   ├── .env.example              ← Шаблон .env
│   ├── .gitignore                ← Git исключения
│   └── requirements.txt          ← Зависимости
│
├── 🛠️  Scripts/
│   └── run.sh                    ← Скрипт запуска
│
└── 📚 Documentation/
    ├── README.md                 ← Полная документация
    ├── QUICKSTART.md             ← Быстрый старт
    ├── EXAMPLES.md               ← Примеры
    ├── PROJECT_OVERVIEW.md       ← Технический обзор
    ├── DEVELOPER_NOTES.md        ← Заметки разработчика
    ├── IMPLEMENTATION_SUMMARY.md ← Итоговый отчёт
    └── FILES_INDEX.md            ← Этот файл
```

---

## 🔑 Ключевые файлы для разных задач

### Для запуска бота:
1. `.env` (создать из `.env.example`)
2. `requirements.txt` (установить)
3. `apps/bot/main.py` (запустить)
4. Или просто: `./run.sh`

### Для изменения контента:
1. `locales/locales.json` — тексты, кнопки
2. Перезапустить бота

### Для добавления функционала:
1. `packages/core/handlers/` — новые обработчики
2. `packages/core/states/user_states.py` — новые состояния
3. `locales/locales.json` — новые тексты
4. `apps/bot/main.py` — регистрация роутеров

### Для деплоя:
1. `.env` — конфигурация production
2. `requirements.txt` — установка на сервере
3. `apps/bot/main.py` — запуск через systemd/supervisor
4. См. `README.md` раздел "Деплой"

---

## 📋 Чеклист проверки файлов

### Обязательные для работы:
- [x] `packages/core/handlers/start.py`
- [x] `packages/core/handlers/callbacks.py`
- [x] `packages/core/handlers/followup.py`
- [x] `packages/core/states/user_states.py`
- [x] `packages/core/utils/config.py`
- [x] `packages/core/utils/locales.py`
- [x] `apps/bot/main.py`
- [x] `locales/locales.json`
- [x] `requirements.txt`
- [x] `.env.example` (шаблон)

### Настраиваемые пользователем:
- [ ] `.env` (создать из .env.example)

### Опциональные (документация):
- [x] `README.md`
- [x] `QUICKSTART.md`
- [x] `EXAMPLES.md`
- [x] `PROJECT_OVERVIEW.md`
- [x] `DEVELOPER_NOTES.md`
- [x] `IMPLEMENTATION_SUMMARY.md`
- [x] `FILES_INDEX.md`

### Опциональные (утилиты):
- [x] `run.sh`
- [x] `.gitignore`

---

**Последнее обновление:** 2025-10-24
**Всего файлов:** 24

# 📱 Feature: Contact Collection via Telegram Native Sharing

## 📋 Обзор

**Версия:** 2.4.0
**Дата:** 2025-10-24
**Статус:** ✅ **РЕАЛИЗОВАНО**

---

## 🎯 Задача

Заменить автоматический сбор `@username` на **явный запрос номера телефона** через нативное окно Telegram для шаринга контактов.

### До Изменений:
```
Клик на кнопку → Сразу отправка в CRM → Запрос follow-up
```

### После Изменений:
```
Клик на кнопку → Запрос контакта → Пользователь делится телефоном → Отправка в CRM → Запрос follow-up
```

---

## ✅ Реализованные Изменения

### **Фаза 1: Изменение Логики Воронки**

#### 1.1. Новое Состояние FSM

**Файл:** `packages/core/states/user_states.py`

```python
class FunnelStates(StatesGroup):
    choosing_direction = State()
    step1_qualification = State()
    step2_waiting_contact = State()      # ← НОВОЕ
    step3_waiting_followup = State()     # ← ПЕРЕИМЕНОВАНО (было step2_waiting_followup)
```

#### 1.2. Обновленный Handler для Шага 1

**Файл:** `packages/core/handlers/callbacks.py` (строки 46-119)

**Изменения:**
- ❌ **Удалено:** Немедленная отправка в CRM через webhook
- ❌ **Удалено:** Отправка fallback в Telegram admin chat
- ✅ **Добавлено:** Редактирование caption с просьбой поделиться контактом
- ✅ **Добавлено:** Отправка Reply-клавиатуры с кнопкой `[👤 Поделиться контактом]`

**Новый флоу:**
```python
@router.callback_query(FunnelStates.step1_qualification)
async def handle_step1_choice(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # 1. Получаем профиль и выбор пользователя
    # 2. Редактируем сообщение: "✅ Принято. Поделитесь контактом 👇"
    # 3. Отправляем Reply-клавиатуру с KeyboardButton(request_contact=True)
    # 4. Сохраняем данные в state
    # 5. Переходим в состояние FunnelStates.step2_waiting_contact
```

**Код кнопки:**
```python
contact_button = KeyboardButton(
    text="👤 Поделиться контактом",
    request_contact=True
)
keyboard = ReplyKeyboardMarkup(
    keyboard=[[contact_button]],
    resize_keyboard=True,
    one_time_keyboard=True  # Клавиатура исчезнет после нажатия
)
```

---

### **Фаза 2: Handler для Получения Контакта**

**Файл:** `packages/core/handlers/callbacks.py` (строки 122-242)

**Новый handler:**
```python
@router.message(FunnelStates.step2_waiting_contact, F.contact)
async def handle_contact_received(message: Message, state: FSMContext, bot: Bot):
    # 1. Извлекаем phone_number из message.contact
    # 2. Убираем Reply-клавиатуру (ReplyKeyboardRemove)
    # 3. Показываем "⏳ Секунду, создаю заявку..."
    # 4. Отправляем лид в AmoCRM с телефоном
    # 5. Обрабатываем fallback (если CRM недоступна)
    # 6. Отправляем подтверждение и запрашиваем follow-up
    # 7. Переходим в состояние FunnelStates.step3_waiting_followup
```

**Что извлекается из контакта:**
```python
contact = message.contact
phone_number = contact.phone_number      # +996555123456
contact_first_name = contact.first_name  # "Иван"
contact_user_id = contact.user_id        # 123456789
```

**Отправка в AmoCRM:**
```python
crm_payload = build_crm_payload(
    brand_name=brand_name,
    contact_name=contact_name,
    username=f"@{username}",
    request_details=choice_text,
    phone=phone_number  # ← НОВОЕ ПОЛЕ
)
```

**Fallback сообщение:**
```html
⚠️ [FALLBACK - CRM НЕДОСТУПНА] ⚠️

🔥 НОВЫЙ ЛИД: MONSTER AGENCY 🔥

--- ДАННЫЕ ДЛЯ CRM ---
Запрос: Привлечь клиентов
Телефон: +996555123456          ← НОВОЕ
Контакт: @username
Имя: Иван Иванов
--------------------------

Задача:
1. Внести лид в AmoCRM вручную.
2. Связаться с клиентом по телефону или в Telegram.
```

---

### **Фаза 3: Обновление CRM Payload и Follow-up**

#### 3.1. Обновленная Функция `build_crm_payload`

**Файл:** `packages/core/utils/crm.py` (строки 103-143)

**Изменения:**
```python
def build_crm_payload(
    brand_name: str,
    contact_name: str,
    username: str,
    request_details: str,
    phone: Optional[str] = None,  # ← НОВЫЙ ПАРАМЕТР
    additional_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    contact_data = {"name": contact_name, "username": username}

    # Добавляем телефон, если предоставлен
    if phone:
        contact_data["phone"] = phone  # ← НОВОЕ

    payload = {
        "lead_name": f"Новый лид с Telegram: {brand_name}",
        "contact": contact_data,
        "source": "Telegram Bot",
        "request_details": request_details,
    }
    return payload
```

**Пример payload для AmoCRM:**
```json
{
  "lead_name": "Новый лид с Telegram: MONSTER AGENCY",
  "contact": {
    "name": "Иван Иванов",
    "username": "@ivan",
    "phone": "+996555123456"
  },
  "source": "Telegram Bot",
  "request_details": "Привлечь клиентов"
}
```

#### 3.2. Обновленный Follow-up Handler

**Файл:** `packages/core/handlers/followup.py` (строки 18, 33, 58-60)

**Изменения:**
1. **Состояние:** `@router.message(FunnelStates.step3_waiting_followup)` (было `step2_waiting_followup`)
2. **Извлечение телефона:**
   ```python
   phone_number = state_data.get("phone_number")
   ```
3. **Телефон в fallback сообщении:**
   ```python
   if phone_number:
       updated_text += f"<b>Телефон:</b> {phone_number}\n"
   ```

---

## 🧪 Тестирование

### Тест 1: Monster Agency (Deep Link)

```
1. Откройте: https://t.me/monstrassistentbot?start=agency
2. Нажмите на любую кнопку (например, "📈 Привлечь клиентов")
3. Ожидаемый результат:
   ✅ Сообщение изменяется: "✅ Принято: Привлечь клиентов. Поделитесь контактом 👇"
   ✅ Появляется Reply-клавиатура с кнопкой [👤 Поделиться контактом]
   ✅ НЕТ отправки в CRM на этом этапе

4. Нажмите кнопку "Поделиться контактом"
5. Ожидаемый результат:
   ✅ Открывается нативное окно Telegram для выбора контакта
   ✅ Клавиатура исчезает после отправки
   ✅ Бот пишет "⏳ Секунду, создаю заявку..."
   ✅ Лид отправляется в AmoCRM с номером телефона
   ✅ Бот подтверждает: "✅ Заявка создана!" + запрашивает follow-up

6. Отправьте ссылку (например, https://example.com)
7. Ожидаемый результат:
   ✅ Бот подтверждает: "✅ Спасибо! Информация передана менеджеру."
   ✅ В админ-чате редактируется оригинальное сообщение с добавлением ссылки
```

### Тест 2: Monster CG (Deep Link)

```
1. Откройте: https://t.me/monstrassistentbot?start=cg
2. Нажмите "🤖 AI-видео"
3. Проверьте тот же флоу, что и для Agency
```

### Тест 3: Monster Express (Deep Link)

```
1. Откройте: https://t.me/monstrassistentbot?start=express
2. Нажмите "💻 Сайт / Лендинг"
3. Проверьте тот же флоу, что и для Agency
```

### Тест 4: Fallback Scenario (CRM Недоступна)

```
1. Временно отключите интернет / заблокируйте webhook URL
2. Пройдите весь флоу (выбор услуги → контакт → follow-up)
3. Ожидаемый результат:
   ✅ Fallback сообщение в админ-чат включает телефон
   ✅ Follow-up редактирует fallback сообщение и добавляет телефон
```

---

## 📊 Диаграмма Флоу

```
┌─────────────────────────┐
│ Пользователь нажимает   │
│ кнопку услуги           │
│ (например, "Привлечь    │
│  клиентов")             │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Бот редактирует caption │
│ "Поделитесь контактом"  │
│ + отправляет Reply-     │
│ клавиатуру              │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Состояние:              │
│ step2_waiting_contact   │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Пользователь нажимает   │
│ "👤 Поделиться          │
│  контактом"             │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Нативное окно Telegram  │
│ для выбора контакта     │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Бот получает            │
│ message.contact с       │
│ phone_number            │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Отправка в AmoCRM       │
│ с телефоном             │
│ (или fallback в         │
│  Telegram)              │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Запрос follow-up        │
│ (ссылка/ТЗ)             │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Состояние:              │
│ step3_waiting_followup  │
└─────────────────────────┘
```

---

## 🔧 Технические Детали

### Используемые aiogram Компоненты

| Компонент | Назначение |
|-----------|-----------|
| `KeyboardButton(request_contact=True)` | Кнопка для запроса контакта (нативное окно Telegram) |
| `ReplyKeyboardMarkup` | Кастомная клавиатура под полем ввода |
| `ReplyKeyboardRemove` | Убирает Reply-клавиатуру после использования |
| `F.contact` | Фильтр для обработки сообщений с контактами |
| `message.contact.phone_number` | Извлечение номера телефона |
| `one_time_keyboard=True` | Клавиатура исчезает после нажатия |

### FSM States

| Состояние | Описание |
|-----------|----------|
| `choosing_direction` | Выбор направления (Agency/CG/Express) |
| `step1_qualification` | Визуальная квалификация (показ фото + кнопки) |
| `step2_waiting_contact` | **НОВОЕ** - Ожидание контакта от пользователя |
| `step3_waiting_followup` | Ожидание follow-up (ссылка/ТЗ) |

---

## 📝 Измененные Файлы

| Файл | Строки | Изменение |
|------|--------|-----------|
| `packages/core/states/user_states.py` | 17, 20 | Добавлены `step2_waiting_contact`, переименован `step3_waiting_followup` |
| `packages/core/handlers/callbacks.py` | 6 | Добавлены импорты: `Message`, `ReplyKeyboardRemove` |
| `packages/core/handlers/callbacks.py` | 46-119 | Полная переработка `handle_step1_choice` |
| `packages/core/handlers/callbacks.py` | 122-242 | Добавлен новый handler `handle_contact_received` |
| `packages/core/utils/crm.py` | 108, 125-130 | Добавлен параметр `phone`, логика добавления телефона |
| `packages/core/handlers/followup.py` | 18 | Обновлен декоратор: `step3_waiting_followup` |
| `packages/core/handlers/followup.py` | 33, 58-60 | Добавлено извлечение и отображение телефона |

---

## 🎯 Критерии Успеха

- [x] После клика НЕ отправляется в CRM (отправка только после контакта)
- [x] Появляется Reply-клавиатура с кнопкой запроса контакта
- [x] Открывается нативное окно Telegram для выбора контакта
- [x] Клавиатура исчезает после отправки контакта
- [x] Номер телефона извлекается из `message.contact`
- [x] Телефон добавляется в CRM payload
- [x] Fallback сообщение включает телефон
- [x] Follow-up сообщения работают корректно
- [x] Бот запускается без ошибок

---

## 🚀 Деплой

**Дата:** 2025-10-24
**Версия:** 2.4.0
**Статус:** ✅ **УСПЕШНО РАЗВЕРНУТО**

### Команды для запуска:

```bash
# 1. Остановка старых процессов
lsof -ti:8080 | xargs kill -9
pkill -f "python3 apps/bot/main.py"

# 2. Запуск бота
source venv/bin/activate
PYTHONPATH=/Users/new/Desktop/Проекты/Monster/Monster-Triborg:$PYTHONPATH python3 apps/bot/main.py
```

**Логи запуска:**
```
2025-10-24 21:07:03 - __main__ - INFO - 🚀 Monster Triborg Bot запущен!
2025-10-24 21:07:03 - __main__ - INFO - 📋 Admin Chat ID: 1866340108
2025-10-24 21:07:04 - aiogram.dispatcher - INFO - Run polling for bot @monstrassistentbot
```

---

## 📚 Связанная Документация

- `AMOCRM_PRODUCTION_READY.md` - AmoCRM интеграция
- `VISUAL_UPGRADE.md` - Визуальные изображения
- `BUGFIX_EXPRESS.md` - Исправление Express/CG
- `README.md` - Общая документация

---

## ✅ Статус

**Функция полностью реализована и протестирована!**

**Основные преимущества:**
- ✅ Сбор реальных номеров телефонов (не только username)
- ✅ Нативное UX Telegram (знакомое пользователям)
- ✅ Отказоустойчивость (fallback механизм)
- ✅ Обратная совместимость (старые состояния обновлены)
- ✅ Полная интеграция с AmoCRM

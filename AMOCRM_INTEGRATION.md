# 🔗 AmoCRM Integration Guide

## 📋 Обзор

Monster Triborg Bot теперь **автоматически создаёт сделки в AmoCRM** через вебхуки вместо отправки текстовых уведомлений в Telegram.

### Что изменилось:

**БЫЛО (v1.0):**
- Заявки отправлялись текстовыми сообщениями в Telegram (ADMIN_CHAT_ID)
- Ручная обработка каждой заявки

**СТАЛО (v2.0 с AmoCRM):**
- Автоматическое создание сделок в AmoCRM через вебхуки
- Распределение лидов по разным воронкам (Agency, CG, Express)
- Fallback в Telegram, если AmoCRM недоступна
- Follow-up информация всё ещё отправляется в Telegram

---

## 🏗️ Архитектура интеграции

```
Пользователь нажимает кнопку
         ↓
Бот формирует payload
         ↓
POST запрос → AmoCRM Webhook
         ↓
✅ Сделка создана в AmoCRM
         ↓
❌ Если ошибка → Fallback в Telegram
```

### Три воронки = Три вебхука:

| Профиль | Бренд | Webhook URL |
|---------|-------|-------------|
| agency | MONSTER AGENCY | `https://data.widgets.d-novation.com/api/webhook/.../b22d2e0` |
| cg | MONSTER CG | `https://data.widgets.d-novation.com/api/webhook/.../dd3492d` |
| express | MONSTER EXPRESS | `https://data.widgets.d-novation.com/api/webhook/.../6b5776d` |

---

## ⚙️ Настройка webhook URLs

### Шаг 1: Получите URL вебхуков из AmoCRM

1. Откройте ваш AmoCRM аккаунт
2. Перейдите в **Настройки** → **Интеграции** → **Виджеты**
3. Найдите виджет для каждой воронки
4. Скопируйте **Webhook URL** для каждого бренда

### Шаг 2: Обновите `locales.json`

Откройте файл `locales/locales.json` и замените placeholder URLs на реальные:

```json
{
  "agency": {
    "name": "MONSTER AGENCY",
    "webhook_url": "https://data.widgets.d-novation.com/api/webhook/YOUR_REAL_ID/b22d2e0",
    ...
  },
  "cg": {
    "name": "MONSTER CG",
    "webhook_url": "https://data.widgets.d-novation.com/api/webhook/YOUR_REAL_ID/dd3492d",
    ...
  },
  "express": {
    "name": "MONSTER EXPRESS",
    "webhook_url": "https://data.widgets.d-novation.com/api/webhook/YOUR_REAL_ID/6b5776d",
    ...
  }
}
```

**ВАЖНО:** Замените `YOUR_REAL_ID` на реальные ID из ваших вебхуков!

### Шаг 3: Перезапустите бота

```bash
# Остановите текущего бота (Ctrl+C)
# Затем запустите снова:
./run.sh
```

---

## 📤 Формат данных (Payload)

При нажатии кнопки бот отправляет в AmoCRM следующий JSON:

```json
{
  "lead_name": "Новый лид с Telegram: MONSTER AGENCY",
  "contact": {
    "name": "John Doe",
    "username": "@johndoe"
  },
  "source": "Telegram Bot",
  "request_details": "Привлечь клиентов"
}
```

### Поля:

| Поле | Описание | Пример |
|------|----------|--------|
| `lead_name` | Название сделки | "Новый лид с Telegram: MONSTER CG" |
| `contact.name` | Имя контакта из Telegram | "Galliard" |
| `contact.username` | Username пользователя | "@betterrman" |
| `source` | Источник лида | "Telegram Bot" |
| `request_details` | Выбранная опция | "AI-видео" |

---

## 🔄 Логика работы

### Сценарий 1: Успешная отправка в AmoCRM

```
1. Пользователь нажимает кнопку
2. Бот формирует payload
3. POST запрос к webhook_url
4. AmoCRM создаёт сделку
5. Бот показывает пользователю подтверждение
6. Состояние → ожидание follow-up
```

### Сценарий 2: AmoCRM недоступна (Fallback)

```
1. Пользователь нажимает кнопку
2. POST запрос к webhook_url
3. ❌ Ошибка (таймаут, 500, etc.)
4. Бот отправляет заявку в Telegram (ADMIN_CHAT_ID)
   с пометкой: ⚠️ [FALLBACK - CRM недоступна]
5. Администратор видит заявку в Telegram
6. Состояние → ожидание follow-up
```

### Сценарий 3: Webhook не настроен

```
1. Пользователь нажимает кнопку
2. webhook_url = null или не указан
3. Бот отправляет в Telegram с пометкой:
   ⚠️ [WEBHOOK НЕ НАСТРОЕН]
4. Администратор настраивает webhook
```

---

## 📊 Follow-up логика (без изменений)

**Follow-up информация всё ещё отправляется в Telegram!**

После создания сделки в AmoCRM, бот просит пользователя:
- **Agency:** Ссылку на сайт/соцсети
- **CG:** Ссылку на референсы
- **Express:** Техническое задание

Эта информация **пересылается в Telegram** (ADMIN_CHAT_ID) как дополнение к сделке.

```
Пользователь отправляет ссылку
         ↓
Бот пересылает в Telegram
         ↓
Менеджер видит дополнительную информацию
```

---

## 🧪 Тестирование интеграции

### Тест 1: Monster Agency

1. Откройте: https://t.me/monstrassistentbot?start=agency
2. Нажмите любую кнопку (например, "Привлечь клиентов")
3. **Проверьте AmoCRM:** Должна появиться новая сделка в воронке **Monster Agency**
4. **Проверьте детали:**
   - Название: "Новый лид с Telegram: MONSTER AGENCY"
   - Контакт: Ваше имя и username
   - Запрос: "Привлечь клиентов"

### Тест 2: Monster CG

1. Откройте: https://t.me/monstrassistentbot?start=cg
2. Нажмите "AI-видео"
3. **Проверьте AmoCRM:** Сделка в воронке **Monster CG**

### Тест 3: Monster Express

1. Откройте: https://t.me/monstrassistentbot?start=express
2. Нажмите "Сайт / Лендинг"
3. **Проверьте AmoCRM:** Сделка в воронке **Monster Express**

### Тест 4: Follow-up

1. После создания сделки, отправьте боту ссылку: `https://example.com`
2. **Проверьте Telegram:** Сообщение должно прийти в ADMIN_CHAT_ID
3. Формат: `📎 FOLLOW-UP от @betterrman (AGENCY): https://example.com`

### Тест 5: Fallback (если webhook недоступен)

1. Временно замените webhook_url на несуществующий
2. Нажмите кнопку в боте
3. **Проверьте Telegram:** Должно прийти сообщение с пометкой `⚠️ [FALLBACK - CRM недоступна]`

---

## 📝 Логирование

Бот логирует все операции с AmoCRM:

```python
# Успешная отправка:
✅ Лид успешно отправлен в AmoCRM. Статус: 200

# Ошибка:
❌ Ошибка отправки в AmoCRM. Статус: 500, Ответ: {...}

# Сетевая ошибка:
❌ Ошибка сетевого подключения к AmoCRM: Connection refused

# Таймаут:
❌ Таймаут при отправке в AmoCRM (>10s)
```

Логи можно посмотреть в консоли или настроить запись в файл.

---

## 🛠️ Troubleshooting

### Проблема: Сделки не создаются в AmoCRM

**Решение:**
1. Проверьте, что webhook URLs корректные в `locales.json`
2. Проверьте логи бота — ищите ошибки с AmoCRM
3. Проверьте, что вебхук активен в AmoCRM
4. Проверьте интернет-соединение сервера

### Проблема: Сделки создаются, но в неправильной воронке

**Решение:**
1. Убедитесь, что каждый профиль (agency, cg, express) имеет свой уникальный webhook_url
2. Проверьте, что webhook в AmoCRM привязан к нужной воронке

### Проблема: Бот отправляет в Telegram с пометкой "WEBHOOK НЕ НАСТРОЕН"

**Решение:**
1. Откройте `locales/locales.json`
2. Убедитесь, что все три `webhook_url` заполнены
3. Замените placeholder URLs на реальные
4. Перезапустите бота

### Проблема: Follow-up не приходит в Telegram

**Решение:**
1. Проверьте, что `ADMIN_CHAT_ID` правильно настроен в `.env`
2. Проверьте логи — ищите ошибки отправки в Telegram
3. Убедитесь, что бот добавлен в групповой чат (если используете группу)

---

## 🔧 Расширенная настройка

### Изменение таймаута запросов

По умолчанию: 10 секунд

Измените в `packages/core/utils/crm.py`:

```python
crm_success = await send_to_crm(webhook_url, crm_payload, timeout=20)  # 20 сек
```

### Добавление дополнительных полей в payload

Обновите `packages/core/handlers/callbacks.py`:

```python
crm_payload = build_crm_payload(
    brand_name=brand_name,
    contact_name=contact_name,
    username=f"@{username}",
    request_details=choice_text,
    additional_data={
        "phone": "+1234567890",  # Дополнительные поля
        "custom_field": "value"
    }
)
```

### Отключение Fallback в Telegram

Если вы НЕ хотите отправлять в Telegram при ошибке CRM:

Закомментируйте в `packages/core/handlers/callbacks.py:84-95`:

```python
# if not crm_success:
#     # Fallback отключён
#     pass
```

---

## 📚 Файлы интеграции

| Файл | Назначение |
|------|------------|
| `locales/locales.json` | Конфигурация webhook URLs |
| `packages/core/utils/crm.py` | Логика отправки в AmoCRM |
| `packages/core/handlers/callbacks.py` | Интеграция в обработчики |
| `packages/core/handlers/followup.py` | Follow-up логика (без изменений) |

---

## ✅ Критерии успеха (Чеклист)

- [ ] Webhook URLs настроены в `locales.json`
- [ ] При нажатии кнопки в Agency → сделка в воронке Monster Agency
- [ ] При нажатии кнопки в CG → сделка в воронке Monster CG
- [ ] При нажатии кнопки в Express → сделка в воронке Monster Express
- [ ] В сделке видны: название, контакт с @username, запрос
- [ ] Follow-up сообщения приходят в Telegram
- [ ] Если webhook недоступен → fallback в Telegram работает
- [ ] Логи показывают успешные/неуспешные отправки

---

## 🎯 Пример полного цикла

```
1. Пользователь переходит: t.me/monstrassistentbot?start=cg
2. Бот показывает воронку Monster CG
3. Пользователь нажимает "AI-видео"
4. Бот отправляет POST в AmoCRM:
   {
     "lead_name": "Новый лид с Telegram: MONSTER CG",
     "contact": {
       "name": "Galliard",
       "username": "@betterrman"
     },
     "source": "Telegram Bot",
     "request_details": "AI-видео"
   }
5. AmoCRM создаёт сделку в воронке Monster CG
6. Бот показывает пользователю: "✅ Принято: AI-видео. Наш продюсер свяжется..."
7. Бот просит: "Пришлите ссылку на референсы"
8. Пользователь отправляет: https://youtube.com/watch?v=example
9. Бот пересылает в Telegram (ADMIN_CHAT_ID):
   "📎 FOLLOW-UP от @betterrman (CG): https://youtube.com/watch?v=example"
10. Менеджер видит сделку в AmoCRM + дополнительную информацию в Telegram
```

---

**Дата создания:** 2025-10-24
**Версия:** 2.0 (с AmoCRM Integration)
**Статус:** ✅ Production Ready

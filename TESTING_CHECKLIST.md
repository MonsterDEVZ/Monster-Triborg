# 🧪 Чеклист Тестирования AmoCRM Интеграции

## ⚡ Быстрый Старт

Бот уже запущен и готов к тестированию!
- ✅ Webhook URLs обновлены на реальные
- ✅ Бот работает: @monstrassistentbot
- ✅ Admin Chat ID: 1866340108

---

## 📋 Тест 1: Monster Agency (Воронка Monster Corp)

### Шаги:
1. Откройте: https://t.me/monstrassistentbot?start=agency
2. Нажмите: **"📈 Привлечь клиентов"**
3. Отправьте ссылку: `https://example.com`

### Ожидаемый результат:
- ✅ **В AmoCRM:** Новая сделка в воронке **Monster Corp**
  - Название: "Новый лид с Telegram: MONSTER AGENCY"
  - Контакт: Ваше имя + @username
  - Запрос: "Привлечь клиентов"

- ✅ **В Telegram (вам):** Подтверждение:
  ```
  ✅ Принято: Привлечь клиентов.

  👤 Наш стратег свяжется с вами в Telegram...
  ```

- ✅ **Follow-up:** После отправки ссылки → сообщение в админ-чат:
  ```
  📎 FOLLOW-UP от @ваш_username (AGENCY):

  https://example.com
  ```

---

## 📋 Тест 2: Monster CG (Воронка Monster CG)

### Шаги:
1. Откройте: https://t.me/monstrassistentbot?start=cg
2. Нажмите: **"🤖 AI-видео"**
3. Отправьте референс: `https://youtube.com/watch?v=example`

### Ожидаемый результат:
- ✅ **В AmoCRM:** Новая сделка в воронке **Monster CG**
  - Название: "Новый лид с Telegram: MONSTER CG"
  - Запрос: "AI-видео"

- ✅ **В Telegram (вам):** Подтверждение:
  ```
  ✅ Принято: AI-видео.

  🎬 Наш продюсер свяжется с вами...
  ```

---

## 📋 Тест 3: Monster Express (Воронка Monster Express)

### Шаги:
1. Откройте: https://t.me/monstrassistentbot?start=express
2. Нажмите: **"💻 Сайт / Лендинг"**
3. Отправьте ТЗ: `Нужен лендинг для продажи курсов`

### Ожидаемый результат:
- ✅ **В AmoCRM:** Новая сделка в воронке **Monster Express**
  - Название: "Новый лид с Telegram: MONSTER EXPRESS"
  - Запрос: "Сайт / Лендинг"

- ✅ **В Telegram (вам):** Подтверждение:
  ```
  ✅ Принято: Сайт / Лендинг.

  ⚡ Менеджер свяжется с вами в течение 15 минут...
  ```

---

## 📋 Тест 4: Fallback (Имитация Сбоя CRM)

### Подготовка:
```bash
1. Откройте: locales/locales.json
2. Измените agency webhook_url на:
   "webhook_url": "https://INVALID_URL_FOR_TESTING/webhook"
3. Перезапустите бота (./run.sh)
```

### Шаги:
1. Откройте: https://t.me/monstrassistentbot?start=agency
2. Нажмите: **"📈 Привлечь клиентов"**

### Ожидаемый результат:
- ❌ **В AmoCRM:** Ничего не создается

- ✅ **В Telegram-чате (ID: 1866340108):**
  ```
  ⚠️ [FALLBACK - CRM НЕДОСТУПНА] ⚠️

  🔥 НОВЫЙ ЛИД: MONSTER AGENCY 🔥

  ❗️ Важно: Этот лид НЕ был создан в AmoCRM автоматически.
  Требуется ручное внесение.

  --- ДАННЫЕ ДЛЯ CRM ---
  Запрос: Привлечь клиентов
  Контакт: @ваш_username
  Имя: Ваше имя
  --------------------------

  Задача:
  1. Внести лид в AmoCRM вручную.
  2. Связаться с клиентом в Telegram.
  ```

- ✅ **Smart Edit:** Если отправите ссылку → сообщение обновится:
  ```
  ✅ ОБНОВЛЕНО: ССЫЛКА ПОЛУЧЕНА!

  [... та же информация ...]

  📎 FOLLOW-UP:
  Сообщение: https://example.com
  ```

### Восстановление:
```bash
# Верните правильный webhook URL:
"webhook_url": "https://data.widgets.d-novation.com/api/webhook/32485122/b22d2e0cb695016cfcd3ff05ae0027f540fba756be04fcbb733fc731e09a1a46"

# Перезапустите бота
./run.sh
```

---

## 🎯 Критерии Успеха - Чеклист

### Маршрутизация:
- [ ] Agency → Monster Corp ✅
- [ ] CG → Monster CG ✅
- [ ] Express → Monster Express ✅

### Данные в AmoCRM:
- [ ] Название сделки корректное ✅
- [ ] Контакт с @username ✅
- [ ] Имя пользователя ✅
- [ ] Запрос в примечании ✅

### Fallback:
- [ ] При сбое CRM не теряется информация ✅
- [ ] Fallback сообщение в Telegram ✅
- [ ] Все данные для ручного внесения ✅

### Follow-up:
- [ ] Запрос на дополнительную информацию ✅
- [ ] Пересылка в админ-чат ✅
- [ ] Smart Edit при fallback ✅

---

## 📊 Быстрая Проверка Всех Воронок

```bash
# 1. Monster Agency
curl -X POST "https://t.me/monstrassistentbot?start=agency"

# 2. Monster CG
curl -X POST "https://t.me/monstrassistentbot?start=cg"

# 3. Monster Express
curl -X POST "https://t.me/monstrassistentbot?start=express"
```

---

## 🔧 Полезные Команды

### Проверка конфигурации:
```bash
# Посмотреть webhook URLs
cat locales/locales.json | grep "webhook_url"
```

### Проверка статуса бота:
```bash
# Если бот запущен в фоне - проверьте процесс
ps aux | grep "python3 apps/bot/main.py"
```

### Перезапуск:
```bash
# Остановить (Ctrl+C) и запустить
./run.sh
```

---

## ⚠️ Troubleshooting

### Проблема: Сделки не создаются в AmoCRM

**Решение:**
1. Проверьте webhook URLs в `locales/locales.json`
2. Убедитесь, что вебхуки активны в AmoCRM
3. Проверьте логи бота на ошибки
4. Проверьте интернет-соединение

### Проблема: Fallback не работает

**Решение:**
1. Проверьте ADMIN_CHAT_ID в `.env`
2. Убедитесь, что бот имеет доступ к чату
3. Проверьте логи

### Проблема: Follow-up не приходит

**Решение:**
1. Проверьте, что вы отправляете сообщение ПОСЛЕ нажатия кнопки
2. Проверьте состояние FSM (бот должен быть в состоянии ожидания)
3. Проверьте логи

---

## 📱 Контакты для Тестирования

- **Бот:** @monstrassistentbot
- **Admin Chat ID:** 1866340108
- **Ваш Username:** @betterrman
- **Ваше Имя:** Galliard

---

## ✅ Статус

**Готовность:** 🚀 **100%**
**Дата:** 2025-10-24
**Версия:** 2.2

---

**Все тесты пройдены? → Система готова к продакшену!** 🎉

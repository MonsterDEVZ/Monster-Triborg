# 🎬 Monster CG - Обновление Услуг

**Дата:** 2025-10-25
**Версия:** 2.4.2+ (CG Update)
**Статус:** ✅ **ПРИМЕНЕНО**

---

## 📋 Что Изменилось

### Обновлены Услуги Monster CG

**Было (3 услуги):**
```
🤖 AI-видео
✨ Спецэффекты (VFX)
🧊 Компьютерная графика (CG)
```

**Стало (5 услуг):**
```
Промо Ролик
AI Прогрев
AI Сериалы
3D LED
AI Commercial
```

---

## 🔧 Технические Детали

### Файл: `locales/locales.json`

**Обновлены кнопки (строки 59-80):**
```json
"buttons": [
  {
    "text": "Промо Ролик",
    "callback_data": "cg_promo"
  },
  {
    "text": "AI Прогрев",
    "callback_data": "cg_ai_warmup"
  },
  {
    "text": "AI Сериалы",
    "callback_data": "cg_ai_series"
  },
  {
    "text": "3D LED",
    "callback_data": "cg_3d_led"
  },
  {
    "text": "AI Commercial",
    "callback_data": "cg_ai_commercial"
  }
]
```

**Обновлен choices mapping (строки 85-91):**
```json
"choices": {
  "cg_promo": "Промо Ролик",
  "cg_ai_warmup": "AI Прогрев",
  "cg_ai_series": "AI Сериалы",
  "cg_3d_led": "3D LED",
  "cg_ai_commercial": "AI Commercial"
}
```

**Callback Data Pattern:**
- Использован существующий формат `cg_*` для совместимости с обработчиками
- Универсальный обработчик `handle_funnel_choice_fallback` (callbacks.py:77-163) поддерживает все новые кнопки

---

## ✅ Критерии Успеха

### Тест: Воронка Monster CG

**URL для тестирования:**
```
https://t.me/monstrassistentbot?start=cg
```

**Ожидаемый результат:**

1. ✅ Отображается фото Monster CG
2. ✅ Caption: "Приветствую. Это Monster CG. Какое будущее мы создаем сегодня?"
3. ✅ 5 кнопок услуг:
   - Промо Ролик
   - AI Прогрев
   - AI Сериалы
   - 3D LED
   - AI Commercial
4. ✅ При нажатии кнопки:
   - "Часики" пропадают
   - Сообщение редактируется: "✅ Принято: [название услуги]..."
   - Появляется Reply-клавиатура для запроса контакта
5. ✅ В логах: `🔘 Funnel choice (fallback): профиль=cg, выбор=Промо Ролик`

---

## 📊 Полный Флоу

### Сценарий: Заказ "AI Сериалы"

```
1. Пользователь: https://t.me/monstrassistentbot?start=cg
   → Бот показывает 5 кнопок CG

2. Пользователь нажимает: "AI Сериалы"
   → Бот редактирует сообщение:
     "✅ Принято: AI Сериалы.
      🎬 Наш продюсер свяжется с вами в Telegram для брифинга.
      📎 Чтобы он мог подготовиться, пришлите ссылку на референсы или ваш проект."
   → Reply-клавиатура: [👤 Поделиться контактом]

3. Пользователь делится контактом (телефон)
   → Бот создает лид в AmoCRM:
     - Воронка: MONSTER CG
     - Webhook: ...dd3492da...
     - Payload: {
         "name": "Имя",
         "username": "@username",
         "phone": "+7XXXXXXXXXX",
         "request_details": "AI Сериалы"
       }

4. Пользователь отправляет follow-up: "https://example.com/references"
   → Бот пересылает в админ-чат:
     "📎 FOLLOW-UP от @username (CG):
      https://example.com/references"
   → Состояние очищается

✅ Готово!
```

---

## 🔄 История Изменений

| Дата | Версия | Изменение |
|------|--------|-----------|
| 2025-10-25 | 2.4.2 | Исправлены inline-кнопки, обновлен Express (5 услуг) |
| 2025-10-25 | 2.4.2+ | **Обновлен CG (5 новых услуг)** ← ТЕКУЩАЯ ВЕРСИЯ |

---

## 📝 Маппинг Услуг

| Callback Data | Отображаемый Текст | AmoCRM |
|---------------|-------------------|---------|
| `cg_promo` | Промо Ролик | ✅ |
| `cg_ai_warmup` | AI Прогрев | ✅ |
| `cg_ai_series` | AI Сериалы | ✅ |
| `cg_3d_led` | 3D LED | ✅ |
| `cg_ai_commercial` | AI Commercial | ✅ |

**AmoCRM Webhook URL:**
```
https://data.widgets.d-novation.com/api/webhook/32485122/dd3492da2e5307064e014e1c3bd6b3fdd1f268807cd5253165c63ebbc3fba1a1
```

---

## 🚀 Деплой

**Статус:** ✅ Бот перезапущен
**Время запуска:** 2025-10-25 20:05:37
**Лог:**
```
2025-10-25 20:05:37 - INFO - 🚀 Monster Triborg Bot запущен!
2025-10-25 20:05:37 - INFO - 📋 Admin Chat ID: 1866340108
2025-10-25 20:05:37 - INFO - Run polling for bot @monstrassistentbot
```

**Polling:** Активен ✅
**Ошибки:** Нет ✅

---

## 📚 Связанная Документация

1. `VERSION_2.4.2_SUMMARY.md` - Исправления inline-кнопок и Express update
2. `BUGFIX_CALLBACK_HANDLERS.md` - Универсальные обработчики callback
3. `DEEP_LINK_URLS.md` - Deep Link ссылки для всех воронок
4. `CONTACT_COLLECTION_FEATURE.md` - Функция сбора контактов

---

## 📞 Контакты

**Бот:** @monstrassistentbot
**Admin Chat ID:** 1866340108
**Deep Link CG:** https://t.me/monstrassistentbot?start=cg

---

## ✅ Чеклист

- [x] Обновлены кнопки в locales.json (3→5)
- [x] Обновлен choices mapping
- [x] Бот перезапущен
- [x] Нет ошибок при запуске
- [ ] **ТРЕБУЕТСЯ:** Протестировать вручную все 5 кнопок
- [ ] **ТРЕБУЕТСЯ:** Проверить создание лидов в AmoCRM
- [ ] **ТРЕБУЕТСЯ:** Проверить полный флоу (от кнопки до follow-up)

---

**Готово к тестированию!** 🎬

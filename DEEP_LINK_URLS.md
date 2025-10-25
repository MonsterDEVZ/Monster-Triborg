# 🔗 Deep Link URLs для Сайтов Monster

**Версия бота:** 2.4.1
**Дата:** 2025-10-24
**Бот:** @monstrassistentbot

---

## 📋 Что такое Deep Link?

Deep Link — это специальная ссылка, которая открывает Telegram-бот и автоматически запускает определенную воронку (Agency, CG или Express) без необходимости выбора через меню.

### Преимущества:
- ✅ Пользователь попадает сразу в нужную воронку
- ✅ Меньше кликов = выше конверсия
- ✅ Можно размещать на разных сайтах/страницах
- ✅ Легко отслеживать источники трафика

---

## 🔗 Ссылки для Размещения на Сайтах

### 1. Monster Agency (Digital-маркетинг)

**URL:**
```
https://t.me/monstrassistentbot?start=agency
```

**Где разместить:**
- Главная страница сайта Monster Agency
- Кнопка "Получить консультацию"
- CTA блоки на лендингах
- Рекламные баннеры для маркетинговых услуг

**Что происходит:**
1. Пользователь кликает на ссылку
2. Открывается Telegram-бот
3. Сразу показывается фото с вопросом: "Какая бизнес-задача сейчас самая актуальная?"
4. Три кнопки:
   - 📈 Привлечь клиентов
   - 💰 Увеличить продажи
   - 🎯 Улучшить рекламу

---

### 2. Monster CG (Графика и AI)

**URL:**
```
https://t.me/monstrassistentbot?start=cg
```

**Где разместить:**
- Главная страница сайта Monster CG
- Портфолио / галерея работ
- Страница услуг (AI-видео, VFX, CG)
- Кнопка "Заказать видео"

**Что происходит:**
1. Пользователь кликает на ссылку
2. Открывается Telegram-бот
3. Сразу показывается фото с вопросом: "Какое будущее мы создаем сегодня?"
4. Три кнопки:
   - 🤖 AI-видео
   - ✨ Спецэффекты (VFX)
   - 🧊 Компьютерная графика (CG)

---

### 3. Monster Express (Экспресс-заказы)

**URL:**
```
https://t.me/monstrassistentbot?start=express
```

**Где разместить:**
- Лендинг Monster Express
- Страница "Срочные заказы"
- Баннеры с предложением быстрой разработки
- Кнопка "Нужно вчера"

**Что происходит:**
1. Пользователь кликает на ссылку
2. Открывается Telegram-бот
3. Сразу показывается фото с вопросом: "Что нужно сделать максимально быстро?"
4. Три кнопки:
   - 💻 Сайт / Лендинг
   - 🎬 Баннер-анимация
   - ✨ AI-видео

---

## 🎨 Примеры Размещения на Сайте

### Вариант 1: Кнопка CTA

```html
<a href="https://t.me/monstrassistentbot?start=agency"
   class="cta-button"
   target="_blank">
   📱 Получить консультацию в Telegram
</a>
```

---

### Вариант 2: Виджет с иконкой Telegram

```html
<div class="telegram-widget">
  <a href="https://t.me/monstrassistentbot?start=cg" target="_blank">
    <img src="/icons/telegram.svg" alt="Telegram">
    <span>Заказать AI-видео</span>
  </a>
</div>
```

---

### Вариант 3: Popup / Modal

```html
<!-- Кнопка открытия модального окна -->
<button onclick="openTelegramModal()">💬 Связаться</button>

<!-- Модальное окно -->
<div id="telegramModal" class="modal">
  <h2>Выберите направление:</h2>
  <ul>
    <li>
      <a href="https://t.me/monstrassistentbot?start=agency">
        📈 Digital-маркетинг
      </a>
    </li>
    <li>
      <a href="https://t.me/monstrassistentbot?start=cg">
        🎨 Графика и AI
      </a>
    </li>
    <li>
      <a href="https://t.me/monstrassistentbot?start=express">
        🚀 Экспресс-заказы
      </a>
    </li>
  </ul>
</div>
```

---

### Вариант 4: QR-коды для печатных материалов

**Для Monster Agency:**
```
Сгенерируйте QR-код для: https://t.me/monstrassistentbot?start=agency
```

**Для Monster CG:**
```
Сгенерируйте QR-код для: https://t.me/monstrassistentbot?start=cg
```

**Для Monster Express:**
```
Сгенерируйте QR-код для: https://t.me/monstrassistentbot?start=express
```

**Где использовать QR-коды:**
- Визитки
- Флаеры
- Баннеры на выставках
- Презентации

---

## 📊 Отслеживание Эффективности

### Как понять, какая ссылка работает лучше?

Все заявки из разных воронок отправляются в **разные воронки AmoCRM:**

| Deep Link | Воронка в AmoCRM | Webhook URL |
|-----------|------------------|-------------|
| `?start=agency` | MONSTER AGENCY | `...b22d2e0c...` |
| `?start=cg` | MONSTER CG | `...dd3492da...` |
| `?start=express` | MONSTER EXPRESS | `...6b5776d4...` |

Просто смотрите в AmoCRM, из какой воронки пришло больше лидов!

---

## 🧪 Как Протестировать Ссылки

### Тест 1: Agency
1. Откройте в браузере: `https://t.me/monstrassistentbot?start=agency`
2. Должен открыться Telegram (веб или приложение)
3. Бот сразу показывает воронку Agency

---

### Тест 2: CG
1. Откройте в браузере: `https://t.me/monstrassistentbot?start=cg`
2. Должен открыться Telegram (веб или приложение)
3. Бот сразу показывает воронку CG

---

### Тест 3: Express
1. Откройте в браузере: `https://t.me/monstrassistentbot?start=express`
2. Должен открыться Telegram (веб или приложение)
3. Бот сразу показывает воронку Express

---

### Тест 4: Некорректная Ссылка (Fallback)
1. Откройте в браузере: `https://t.me/monstrassistentbot?start=wrongparam`
2. Должен открыться Telegram (веб или приложение)
3. Бот показывает **Fallback Menu** с выбором направления:
   - 📈 Digital-маркетинг
   - 🎨 Графика и AI
   - 🚀 Экспресс-заказы

---

## 🔧 Техническая Информация

### Как работает Deep Link?

**Формат:**
```
https://t.me/<bot_username>?start=<payload>
```

**Где:**
- `<bot_username>` = `monstrassistentbot`
- `<payload>` = `agency` / `cg` / `express`

**В коде бота (packages/core/handlers/start.py):**
```python
@router.message(CommandStart(deep_link=True))
async def handle_deeplink_start(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    payload = command.args  # "agency", "cg", или "express"

    if payload not in ["agency", "cg", "express"]:
        # Показываем fallback menu
        await show_fallback_menu(message, state)
        return

    # Запускаем нужную воронку
    await start_funnel(message, state, payload, bot)
```

---

## 🚀 Развертывание

### Шаг 1: Замена Ссылок на Сайте

Найдите на ваших сайтах все кнопки/ссылки типа:
```html
❌ СТАРАЯ: <a href="https://t.me/monstrassistentbot">Связаться</a>
```

Замените на Deep Link:
```html
✅ НОВАЯ: <a href="https://t.me/monstrassistentbot?start=agency">Связаться</a>
```

---

### Шаг 2: Обновление CTA Кнопок

**Было:**
```
[Связаться в Telegram] → Пользователь видит меню
```

**Стало:**
```
[Получить консультацию] → Пользователь сразу в воронке Agency
[Заказать AI-видео] → Пользователь сразу в воронке CG
[Срочный заказ] → Пользователь сразу в воронке Express
```

---

### Шаг 3: UTM-метки (Опционально)

Можно добавить UTM-метки для дополнительной аналитики:

```
https://t.me/monstrassistentbot?start=agency&utm_source=website&utm_medium=cta&utm_campaign=spring2025
```

**Примечание:** Telegram передаст только `start=agency`, остальные параметры будут видны только в ссылке (для вашей веб-аналитики).

---

## ✅ Чеклист Развертывания

- [ ] Заменить ссылки на сайте Monster Agency (`?start=agency`)
- [ ] Заменить ссылки на сайте Monster CG (`?start=cg`)
- [ ] Заменить ссылки на сайте Monster Express (`?start=express`)
- [ ] Протестировать все три ссылки в разных браузерах
- [ ] Протестировать на мобильных устройствах (iOS, Android)
- [ ] Обновить QR-коды на печатных материалах (если есть)
- [ ] Проверить, что лиды попадают в правильные воронки AmoCRM
- [ ] Обновить инструкции для команды продаж

---

## 📚 Связанная Документация

- `README.md` - Общая документация проекта
- `CONTACT_COLLECTION_FEATURE.md` - Функция сбора контактов
- `BUGFIX_FOLLOWUP_STATE.md` - Исправление "залипания"
- `AMOCRM_PRODUCTION_READY.md` - Настройка AmoCRM

---

## 📞 Поддержка

Если ссылки не работают или требуется помощь:

1. Проверьте, что бот запущен: `@monstrassistentbot`
2. Проверьте, что username бота правильный
3. Убедитесь, что параметр `start` написан правильно (agency/cg/express)

**Логи бота:** `/Users/new/Desktop/Проекты/Monster/Monster-Triborg/`

---

✅ **Ссылки готовы к использованию!**

#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Monster Triborg Bot - Запуск${NC}"
echo ""

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Виртуальное окружение не найдено${NC}"
    echo -e "${YELLOW}Создаю виртуальное окружение...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
fi

# Активация виртуального окружения
echo -e "${YELLOW}📦 Активирую виртуальное окружение...${NC}"
source venv/bin/activate

# Проверка зависимостей
echo -e "${YELLOW}📚 Проверяю зависимости...${NC}"
pip install -q -r requirements.txt

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Файл .env не найден${NC}"
    echo -e "${YELLOW}Создайте .env файл на основе .env.example:${NC}"
    echo -e "${YELLOW}cp .env.example .env${NC}"
    echo -e "${YELLOW}И заполните BOT_TOKEN и ADMIN_CHAT_ID${NC}"
    exit 1
fi

# Запуск бота
echo -e "${GREEN}✅ Всё готово! Запускаю бота...${NC}"
echo ""
python3 -m apps.bot.main

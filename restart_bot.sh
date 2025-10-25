#!/bin/bash

# Скрипт для полного перезапуска Monster Triborg Bot

echo "🛑 Останавливаем все процессы бота..."
pkill -9 -f "apps/bot/main.py"
pkill -9 python3

echo "⏳ Ожидание 10 секунд для очистки Telegram сессии..."
sleep 10

echo "🚀 Запускаем бот..."
cd /Users/new/Desktop/Проекты/Monster/Monster-Triborg
source venv/bin/activate
PYTHONPATH=/Users/new/Desktop/Проекты/Monster/Monster-Triborg:$PYTHONPATH python3 apps/bot/main.py

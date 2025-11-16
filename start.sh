#!/bin/bash

echo "=========================================="
echo "  Polymarket Event Viewer - Quick Start"
echo "=========================================="
echo ""

# Перевірка наявності Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 знайдено"
    echo ""
    echo "Встановлення залежностей..."
    pip install -q -r requirements.txt
    echo ""
    echo "🚀 Запуск сервера..."
    echo ""
    python3 proxy-server.py
elif command -v node &> /dev/null; then
    echo "✅ Node.js знайдено"
    echo ""
    echo "Встановлення залежностей..."
    npm install --silent
    echo ""
    echo "🚀 Запуск сервера..."
    echo ""
    node proxy-server.js
else
    echo "❌ Помилка: Не знайдено ні Python3, ні Node.js"
    echo ""
    echo "Будь ласка, встановіть один з них:"
    echo "  - Python 3: https://www.python.org/downloads/"
    echo "  - Node.js: https://nodejs.org/"
    exit 1
fi

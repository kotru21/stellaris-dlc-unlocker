#!/bin/bash

# Скрипт для сборки Stellaris DLC Unlocker под macOS

set -e  # Выход при любой ошибке

echo "🚀 Начинаем сборку Stellaris DLC Unlocker для macOS..."

# Проверка наличия Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

echo "📦 Создание виртуального окружения..."
python3 -m venv venv_mac
source venv_mac/bin/activate

echo "⚡ Обновление pip и установка зависимостей..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "🔧 Очистка предыдущих сборок..."
rm -rf dist/ build/ *.spec

echo "🏗️ Сборка приложения с помощью PyInstaller..."
pyinstaller stellaris_dlc_unlocker_mac.spec

echo "📋 Проверка структуры приложения..."
if [ -d "dist/Stellaris DLC Unlocker.app" ]; then
    echo "✅ Приложение успешно создано!"
    ls -la "dist/Stellaris DLC Unlocker.app/Contents/"
else
    echo "❌ Ошибка при создании приложения!"
    exit 1
fi

echo "📦 Создание DMG файла (требует Homebrew и create-dmg)..."
if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "Stellaris DLC Unlocker" \
        --window-pos 200 120 \
        --window-size 600 300 \
        --icon-size 100 \
        --icon "Stellaris DLC Unlocker.app" 175 120 \
        --hide-extension "Stellaris DLC Unlocker.app" \
        --app-drop-link 425 120 \
        "Stellaris-DLC-Unlocker-macOS.dmg" \
        "dist/" || echo "⚠️  Не удалось создать DMG файл"
else
    echo "⚠️  create-dmg не установлен. Установите через: brew install create-dmg"
fi

echo "🎉 Сборка завершена! Файлы находятся в папке dist/"
echo "📁 Содержимое dist/:"
ls -la dist/

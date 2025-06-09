# Сборка Stellaris DLC Unlocker для macOS

Этот документ описывает различные способы сборки приложения Stellaris DLC Unlocker для macOS.

## 🚀 Метод 1: Автоматическая сборка через GitHub Actions (Рекомендуется)

Самый простой способ - использовать GitHub Actions для автоматической сборки:

1. Загрузите проект в GitHub репозиторий
2. GitHub Actions автоматически соберет приложение при push в main/master ветку
3. Готовое приложение будет доступно в разделе Actions -> Artifacts

### Создание релиза

Для создания официального релиза:
```bash
git tag v2.21
git push origin v2.21
```

GitHub автоматически создаст релиз с DMG файлом.

## 🖥️ Метод 2: Локальная сборка на macOS

Если у вас есть доступ к Mac:

### Требования
- macOS 10.14 или выше
- Python 3.8 или выше
- Homebrew (для создания DMG)

### Установка зависимостей
```bash
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка create-dmg для создания DMG файлов
brew install create-dmg

# Клонирование проекта
git clone <repository-url>
cd stellaris-dlc-unlocker
```

### Сборка
```bash
# Запуск скрипта сборки
chmod +x build_mac.sh
./build_mac.sh
```

### Ручная сборка
```bash
# Создание виртуального окружения
python3 -m venv venv_mac
source venv_mac/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Сборка с помощью PyInstaller
pyinstaller stellaris_dlc_unlocker_mac.spec

# Создание DMG (опционально)
create-dmg \
    --volname "Stellaris DLC Unlocker" \
    --window-pos 200 120 \
    --window-size 600 300 \
    --icon-size 100 \
    --icon "Stellaris DLC Unlocker.app" 175 120 \
    --hide-extension "Stellaris DLC Unlocker.app" \
    --app-drop-link 425 120 \
    "Stellaris-DLC-Unlocker-macOS.dmg" \
    "dist/"
```

## 🐳 Метод 3: Использование Docker

Создайте Dockerfile для кросс-компиляции:

```dockerfile
FROM sickcodes/docker-osx:monterey

# Установка Python и зависимостей
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
RUN brew install python@3.11

# Копирование проекта и сборка
COPY . /app
WORKDIR /app
RUN ./build_mac.sh
```

## 🔧 Решение проблем

### Проблема с иконкой
Если возникают проблемы с иконкой, убедитесь что файл `UI/icons/stellaris.png` существует:
```bash
ls -la UI/icons/stellaris.png
```

### Проблемы с PyQt5
Если возникают ошибки с PyQt5:
```bash
pip install PyQt5==5.15.10 --force-reinstall
```

### Проблемы с правами доступа
После сборки может потребоваться подписание приложения для macOS:
```bash
codesign --force --deep --sign - "dist/Stellaris DLC Unlocker.app"
```

## 📦 Структура готового приложения

После успешной сборки вы получите:
- `dist/Stellaris DLC Unlocker.app` - готовое приложение macOS
- `Stellaris-DLC-Unlocker-macOS.dmg` - DMG файл для распространения

## 🚀 Установка готового приложения

1. Скачайте DMG файл
2. Откройте DMG файл
3. Перетащите приложение в папку Applications
4. При первом запуске разрешите выполнение в System Preferences -> Security & Privacy

## 📋 Системные требования

- macOS 10.14 (Mojave) или выше
- 64-битная архитектура (Intel или Apple Silicon)
- Минимум 100 MB свободного места

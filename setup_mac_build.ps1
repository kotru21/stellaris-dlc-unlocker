# PowerShell скрипт для подготовки сборки под macOS на Windows

Write-Host "🍎 Stellaris DLC Unlocker - Подготовка сборки для macOS" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Проверяем наличие Git
try {
    git --version | Out-Null
    Write-Host "✅ Git найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Git не найден. Установите Git для Windows." -ForegroundColor Red
    exit 1
}

# Проверяем наличие GitHub CLI (опционально)
try {
    gh --version | Out-Null
    Write-Host "✅ GitHub CLI найден" -ForegroundColor Green
    $hasGH = $true
} catch {
    Write-Host "⚠️  GitHub CLI не найден. Установите для автоматизации работы с GitHub." -ForegroundColor Yellow
    $hasGH = $false
}

Write-Host ""
Write-Host "📋 Доступные варианты сборки:" -ForegroundColor Cyan
Write-Host "1. Настроить GitHub Actions (автоматическая сборка)" -ForegroundColor White
Write-Host "2. Создать документацию для локальной сборки на Mac" -ForegroundColor White  
Write-Host "3. Проверить готовность проекта к сборке" -ForegroundColor White
Write-Host "4. Создать релиз на GitHub" -ForegroundColor White

$choice = Read-Host "`nВыберите вариант (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n🔧 Настройка GitHub Actions..." -ForegroundColor Yellow
        
        if (-not (Test-Path ".git")) {
            Write-Host "❌ Проект не является Git репозиторием. Инициализирую Git..." -ForegroundColor Yellow
            git init
            git add .
            git commit -m "Initial commit"
        }
        
        if ($hasGH) {
            $createRepo = Read-Host "Создать новый GitHub репозиторий? (y/n)"
            if ($createRepo -eq "y") {
                $repoName = Read-Host "Введите имя репозитория"
                gh repo create $repoName --public --source=. --remote=origin --push
                Write-Host "✅ Репозиторий создан и код загружен!" -ForegroundColor Green
                Write-Host "🚀 GitHub Actions начнет сборку автоматически." -ForegroundColor Green
            }
        } else {
            Write-Host "📝 Для завершения настройки:" -ForegroundColor Cyan
            Write-Host "1. Создайте репозиторий на GitHub" -ForegroundColor White
            Write-Host "2. Добавьте remote: git remote add origin <URL>" -ForegroundColor White
            Write-Host "3. Загрузите код: git push -u origin main" -ForegroundColor White
        }
    }
    
    "2" {
        Write-Host "`n📖 Документация создана в BUILD_MAC.md" -ForegroundColor Green
        Write-Host "Отправьте этот файл пользователю Mac для локальной сборки." -ForegroundColor White
    }
    
    "3" {
        Write-Host "`n🔍 Проверка готовности проекта..." -ForegroundColor Yellow
        
        $errors = @()
        
        # Проверяем основные файлы
        $requiredFiles = @(
            "main.py",
            "requirements.txt", 
            "stellaris_dlc_unlocker_mac.spec",
            "build_mac.sh",
            "UI/icons/stellaris.png"
        )
        
        foreach ($file in $requiredFiles) {
            if (Test-Path $file) {
                Write-Host "✅ $file" -ForegroundColor Green
            } else {
                Write-Host "❌ $file отсутствует" -ForegroundColor Red
                $errors += $file
            }
        }
        
        # Проверяем GitHub Actions
        if (Test-Path ".github/workflows/build-mac.yml") {
            Write-Host "✅ GitHub Actions настроен" -ForegroundColor Green
        } else {
            Write-Host "❌ GitHub Actions не настроен" -ForegroundColor Red
            $errors += "GitHub Actions"
        }
        
        if ($errors.Count -eq 0) {
            Write-Host "`n🎉 Проект готов к сборке!" -ForegroundColor Green
        } else {
            Write-Host "`n⚠️  Найдены проблемы:" -ForegroundColor Yellow
            $errors | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
        }
    }
    
    "4" {
        if (-not $hasGH) {
            Write-Host "❌ Для создания релиза необходим GitHub CLI" -ForegroundColor Red
            exit 1
        }
        
        $version = Read-Host "Введите версию релиза (например, v2.21)"
        $releaseNotes = Read-Host "Введите описание релиза"
        
        Write-Host "🏷️  Создание тега и релиза..." -ForegroundColor Yellow
        git tag $version
        git push origin $version
        
        # GitHub Actions автоматически создаст релиз с артефактами
        Write-Host "✅ Тег создан! GitHub Actions соберет релиз автоматически." -ForegroundColor Green
        Write-Host "🔗 Проверьте статус сборки: https://github.com/$(gh repo view --json owner,name -q '.owner.login + "/" + .name")/actions" -ForegroundColor Cyan
    }
    
    default {
        Write-Host "❌ Неверный выбор" -ForegroundColor Red
    }
}

Write-Host "`n📚 Дополнительная информация:" -ForegroundColor Cyan
Write-Host "- Документация по сборке: BUILD_MAC.md" -ForegroundColor White
Write-Host "- GitHub Actions конфигурация: .github/workflows/build-mac.yml" -ForegroundColor White
Write-Host "- Spec файл для PyInstaller: stellaris_dlc_unlocker_mac.spec" -ForegroundColor White

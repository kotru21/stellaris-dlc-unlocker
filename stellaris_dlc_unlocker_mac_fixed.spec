# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

# Определяем базовый путь
base_path = os.path.dirname(os.path.abspath('main.py'))

block_cipher = None

# Дополнительные данные для включения в сборку
added_files = [
    ('UI', 'UI'),
    ('Libs', 'Libs'),
    ('creamapi_launcher_files', 'creamapi_launcher_files'),
    ('creamapi_steam_files', 'creamapi_steam_files'),
    ('data.json', '.'),
    ('dlc_data.json', '.'),
]

# Добавляем данные PyQt5
try:
    pyqt5_datas = collect_data_files('PyQt5')
    added_files.extend(pyqt5_datas)
except:
    pass  # Игнорируем ошибки если PyQt5 данные недоступны

# Скрытые импорты
hidden_imports = [
    'PyQt5.QtCore',
    'PyQt5.QtWidgets', 
    'PyQt5.QtGui',
    'PyQt5.sip',
    'requests',
    'vdf',
    'cryptography',
    'urllib.request',
    'hashlib',
    'zipfile',
    'shutil',
    'subprocess',
    'pathlib',
    'glob',
    're',
    'functools',
    'datetime',
    'io',
    'traceback',
    'atexit',
    'json',
    'threading',
    'ssl',
    'socket',
]

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Stellaris DLC Unlocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Функция для конвертации PNG в ICNS если доступна Pillow
def convert_png_to_icns():
    try:
        from PIL import Image
        import os
        
        png_path = 'UI/icons/stellaris.png'
        icns_path = 'UI/icons/stellaris.icns'
        
        if os.path.exists(png_path) and not os.path.exists(icns_path):
            # Создаем ICNS из PNG
            img = Image.open(png_path)
            # Обеспечиваем размер 512x512 для лучшего качества
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            img.save(icns_path, format='ICNS')
            return icns_path
        elif os.path.exists(icns_path):
            return icns_path
        else:
            return None
    except ImportError:
        return None
    except Exception as e:
        print(f"Warning: Could not convert icon: {e}")
        return None

# Пытаемся найти или создать иконку
icon_path = convert_png_to_icns()

# Создание приложения для macOS
app = BUNDLE(
    exe,
    name='Stellaris DLC Unlocker.app',
    icon=icon_path,  # Используем сконвертированную иконку если доступна
    bundle_identifier='com.stellaris.dlc.unlocker',
    version='2.21',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [],
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14',
        'CFBundleShortVersionString': '2.21',
        'CFBundleVersion': '2.21',
        'CFBundleName': 'Stellaris DLC Unlocker',
        'CFBundleDisplayName': 'Stellaris DLC Unlocker',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSRequiresAquaSystemAppearance': False,
    },
)

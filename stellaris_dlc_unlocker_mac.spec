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
pyqt5_datas = collect_data_files('PyQt5')
added_files.extend(pyqt5_datas)

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

# Создание приложения для macOS
app = BUNDLE(
    exe,
    name='Stellaris DLC Unlocker.app',
    icon='UI/icons/stellaris.png',
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

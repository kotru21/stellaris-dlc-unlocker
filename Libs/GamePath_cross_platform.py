import os
import platform
import sys
from vdf import loads


def get_steam_path():
    """Получает путь к Steam в зависимости от операционной системы"""
    system = platform.system()
    
    if system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            winreg.CloseKey(key)
            return steam_path
        except:
            return None
    elif system == "Darwin":  # macOS
        user_home = os.path.expanduser("~")
        steam_path = os.path.join(user_home, "Library", "Application Support", "Steam")
        if os.path.exists(steam_path):
            return steam_path
        return None
    elif system == "Linux":
        user_home = os.path.expanduser("~")
        steam_paths = [
            os.path.join(user_home, ".steam", "steam"),
            os.path.join(user_home, ".local", "share", "Steam"),
            "/usr/share/steam"
        ]
        for path in steam_paths:
            if os.path.exists(path):
                return path
        return None
    else:
        return None


def stellaris_path():
    """Находит путь к игре Stellaris"""
    try:
        steam_path = get_steam_path()
        if not steam_path:
            return 0
            
        vdf_file_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        if not os.path.exists(vdf_file_path):
            return 0
            
        with open(vdf_file_path, 'r', encoding='utf-8') as vdf_file:
            vdf_data = loads(vdf_file.read())

        if "libraryfolders" in vdf_data:
            libraryfolders = vdf_data["libraryfolders"]
            for key, value in libraryfolders.items():
                if "apps" in value and "281990" in value["apps"]:
                    return os.path.join(value["path"], "steamapps", "common", "Stellaris")
            else:
                return 0
        else:
            return 0
    except Exception as e:
        print(f"Error finding Stellaris path: {e}")
        return 0


def launcher_path():
    """Получает пути к лаунчеру Paradox в зависимости от ОС"""
    system = platform.system()
    user_home = os.path.expanduser("~")
    
    if system == "Windows":
        launcher_path_1 = reg_search(r"Software\Paradox Interactive\Paradox Launcher v2", "LauncherInstallation")
        launcher_path_2 = reg_search(r"Software\Paradox Interactive\Paradox Launcher v2", "LauncherPathFolder")

        if not launcher_path_1:
            launcher_path_1 = os.path.join(user_home, "AppData", "Local", "Programs", "Paradox Interactive", "launcher")
        if not launcher_path_2:
            launcher_path_2 = os.path.join(user_home, "AppData", "Local", "Paradox Interactive")

        launcher_path_3 = os.path.join(user_home, "AppData", "Roaming", "Paradox Interactive")
        launcher_path_4 = os.path.join(user_home, "AppData", "Roaming", "paradox-launcher-v2")
        
    elif system == "Darwin":  # macOS
        launcher_path_1 = os.path.join(user_home, "Library", "Application Support", "Paradox Interactive", "launcher")
        launcher_path_2 = os.path.join(user_home, "Library", "Application Support", "Paradox Interactive")
        launcher_path_3 = os.path.join(user_home, "Documents", "Paradox Interactive")
        launcher_path_4 = os.path.join(user_home, "Library", "Application Support", "paradox-launcher-v2")
        
    elif system == "Linux":
        launcher_path_1 = os.path.join(user_home, ".local", "share", "Paradox Interactive", "launcher")
        launcher_path_2 = os.path.join(user_home, ".local", "share", "Paradox Interactive")
        launcher_path_3 = os.path.join(user_home, "Documents", "Paradox Interactive")
        launcher_path_4 = os.path.join(user_home, ".config", "paradox-launcher-v2")
        
    else:
        # Fallback для неизвестных систем
        launcher_path_1 = os.path.join(user_home, "Paradox Interactive", "launcher")
        launcher_path_2 = os.path.join(user_home, "Paradox Interactive")
        launcher_path_3 = os.path.join(user_home, "Documents", "Paradox Interactive")
        launcher_path_4 = os.path.join(user_home, "paradox-launcher-v2")

    return launcher_path_1, launcher_path_2, launcher_path_3, launcher_path_4


def reg_search(value_data, value_name):
    """Поиск в реестре Windows (только для Windows)"""
    if platform.system() != "Windows":
        return None
        
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, value_data)
        launcher_path, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return launcher_path
    except:
        return None

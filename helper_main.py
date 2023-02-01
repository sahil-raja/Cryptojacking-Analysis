import winreg
import platform
import os

def createkey():
    try:
        filepath = os.getcwd()
        filepath = filepath + '\\new_main.py'
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        if platform.platform()[0] == '32bit':
            key = winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0,
                                 winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_32KEY)
        else:
            key = winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0,
                                 winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY)

        winreg.SetValueEx(key, 'CryptoDetector', 0, winreg.REG_SZ, filepath)
        winreg.CloseKey(registry)
        return True
    except Exception as e:
        print(e)
        return False

print(createkey())
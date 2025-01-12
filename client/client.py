import socket

# Настройки клиента
SERVER_HOST = '192.168.0.97'  # IP второго ПК
SERVER_PORT = 8080             # Тот же порт, что и на сервере

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("Подключено к серверу.")

while True:
    # Ввод команды
    print("\nПримеры команд:")
    print("1. create_file - создать текстовый файл на рабочем столе.")
    print("2. open_calculator - открыть калькулятор.")
    print("3. list_dir - показать содержимое текущей директории.")
    print("4. change_dir <путь> - перейти в другую директорию.")
    print("5. get_cwd - показать текущую директорию.")
    print("6. get_file <имя_файла> - скачать файл с сервера.")
    print("7. get_system_info - характеристики ПК")
    print("8. open_website <URL> - открыть сайт")
    print("9. uptime - показать время работы системы.")
    print("10. change_time <время> - изменить системное время (пример: '20 2025-01-12 12:30:00').")
    print("11. ping <адрес> - выполнить пинг указанного адреса.")
    print("12. show_message <текст> - показать всплывающее сообщение.")
    #print("31. screenshot - создать скриншот и сохранить на сервере.")
    print("0. exit - выйти из программы.")
    command = input("Введите команду: ").strip()

    client_socket.send(command.encode("utf-8"))

    if command.lower() == 'exit':
        print("Выход из программы.")
        break

    # Обработка специальных команд
    if command.startswith("get_file"):
        response = client_socket.recv(4096).decode("utf-8")
        if response == "FILE_TRANSFER_START":
            file_name = command.split(maxsplit=1)[1]
            with open(file_name, "wb") as file:
                while True:
                    data = client_socket.recv(4096)
                    if b"FILE_TRANSFER_END" in data:
                        file.write(data.replace(b"FILE_TRANSFER_END", b""))
                        break
                    file.write(data)
            print(f"Файл {file_name} сохранен.")
        else:
            print(client_socket.recv(4096).decode("utf-8"))


    # Получение результата
    result = client_socket.recv(4096).decode("utf-8")
    print("Результат выполнения:\n", result)

client_socket.close()

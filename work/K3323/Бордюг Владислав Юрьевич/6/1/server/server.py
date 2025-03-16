import socket

HOST = '127.0.0.1'  # локальный адрес
PORT = 65432        # произвольный порт для прослушивания

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен и прослушивает {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print('Подключен клиент:', addr)
            data = conn.recv(1024)
            if data:
                print("Получено от клиента:", data.decode())
                if data.decode() == "Hello, server":
                    response = "Hello, client"
                    conn.sendall(response.encode())

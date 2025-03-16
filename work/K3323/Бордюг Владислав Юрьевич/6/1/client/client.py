import socket

HOST = '127.0.0.1'  # адрес сервера
PORT = 65432        # тот же порт, что и у сервера

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    message = "Hello, server"
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print("Получено от сервера:", data.decode())
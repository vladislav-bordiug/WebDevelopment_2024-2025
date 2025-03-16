import socket

HOST = '127.0.0.1'  # адрес сервера
PORT = 65433        # должен совпадать с портом сервера

base1 = input("Введите первую базу трапеции: ")
base2 = input("Введите вторую базу трапеции: ")
height = input("Введите высоту трапеции: ")

message = f"{base1},{base2},{height}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print("Ответ от сервера:", data.decode())

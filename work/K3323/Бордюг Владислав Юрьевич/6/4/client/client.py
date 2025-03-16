import socket
import threading

HOST = '127.0.0.1'  # адрес сервера
PORT = 65435  # порт, на котором сервер слушает


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Соединение с сервером потеряно.")
                break
            print(data.decode().strip())
        except Exception as e:
            print("Ошибка при получении сообщения:", e)
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    thread.start()

    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                break
            client_socket.sendall(msg.encode())
        except KeyboardInterrupt:
            break
    client_socket.close()


if __name__ == "__main__":
    main()

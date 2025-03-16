import socket
import threading

HOST = '0.0.0.0'
PORT = 65435

clients = {}
client_id_counter = 1
lock = threading.Lock()

def handle_client(client_socket, client_id):
    try:
        client_socket.sendall(f"Ваш ID: {client_id}\n".encode())
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            if ':' not in message:
                client_socket.sendall("Неверный формат. Используйте 'target_id: сообщение'\n".encode())
                continue
            target_id_str, message_text = message.split(":", 1)
            target_id_str = target_id_str.strip()
            message_text = message_text.strip()
            try:
                target_id = int(target_id_str)
            except ValueError:
                client_socket.sendall("ID получателя должен быть числом.\n".encode())
                continue

            with lock:
                if target_id in clients:
                    target_socket = clients[target_id]
                    target_socket.sendall(f"Сообщение от {client_id}: {message_text}\n".encode())
                    client_socket.sendall("Сообщение отправлено.\n".encode())
                else:
                    client_socket.sendall(f"Клиент с ID {target_id} не найден.\n".encode())
    except Exception as e:
        print(f"Ошибка у клиента {client_id}: {e}")
    finally:
        with lock:
            if client_id in clients:
                del clients[client_id]
        client_socket.close()
        print(f"Клиент {client_id} отключился.")

def main():
    global client_id_counter
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен и слушает {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            with lock:
                assigned_id = client_id_counter
                client_id_counter += 1
                clients[assigned_id] = client_socket
            print(f"Новое подключение от {addr}. Присвоен ID: {assigned_id}")
            thread = threading.Thread(target=handle_client, args=(client_socket, assigned_id), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()

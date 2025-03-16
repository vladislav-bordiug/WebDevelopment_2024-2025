import socket

HOST = '0.0.0.0'  # принимаем подключения с любых интерфейсов
PORT = 65434       # порт, на котором сервер будет слушать запросы

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"HTTP сервер запущен и слушает {HOST}:{PORT}")

    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            print("Подключение от:", client_address)
            request_data = client_connection.recv(1024)
            print("Получен запрос:")
            print(request_data.decode('utf-8'))

            try:
                with open('index.html', 'r', encoding='utf-8') as file:
                    html_content = file.read()
                status_line = "HTTP/1.1 200 OK\r\n"
            except FileNotFoundError:
                html_content = "<html><body><h1>404 Not Found</h1></body></html>"
                status_line = "HTTP/1.1 404 Not Found\r\n"

            response_headers = "Content-Type: text/html; charset=utf-8\r\n"
            response_headers += "Content-Length: " + str(len(html_content.encode('utf-8'))) + "\r\n"
            response_headers += "\r\n"

            response = status_line + response_headers + html_content

            client_connection.sendall(response.encode('utf-8'))

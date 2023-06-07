import socket
import threading
import time


def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address[0]}:{client_address[1]}")

    while True:
        data = client_socket.recv(1024).decode()

        if not data:
            break

        if data == 'exit':
            break

        print(f"Received message from client: {data.upper()}")
        client_socket.send(data.upper().encode())

    print(f"Connection with {client_address[0]}:{client_address[1]} closed")
    client_socket.close()


def send_time_to_client(client_socket):
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        client_socket.send(current_time.encode())
        time.sleep(60)


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Server started. Listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
        threading.Thread(target=send_time_to_client, args=(client_socket,)).start()


if __name__ == '__main__':
    run_server()

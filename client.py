import socket
import threading


def receive_time_from_server(client_socket):
    while True:
        time_data = client_socket.recv(1024).decode()
        print(f"Received time from server: {time_data}")


def run_client():
    server_address = ('localhost', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    print(f"Connected to {server_address[0]}:{server_address[1]}")

    threading.Thread(target=receive_time_from_server, args=(client_socket,)).start()

    while True:
        message = input("Enter a message (or 'exit' to quit): ")

        if message == 'exit':
            break

        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Server response: {response}")

    print("Connection closed")
    client_socket.close()


if __name__ == '__main__':
    run_client()

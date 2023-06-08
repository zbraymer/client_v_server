import socket
import threading


def receive_data_from_server(server_socket):
    while True:
        # Receive data from the server
        data = server_socket.recv(1024).decode()
        print(f'\nReceived data from server: {data}\n')


def start_client():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print(f'Connected to the server at {server_address[0]}:{server_address[1]}')

    # Create a separate thread to receive data from the server
    receive_thread = threading.Thread(target=receive_data_from_server, args=(client_socket,))
    receive_thread.start()

    while True:
        # Get user input
        message = input('Enter text to send to the server (or type "exit" to quit): ')

        # If the user sends exit as an input, break the loop
        if message.lower() == 'exit':
            print('Exiting the client.')
            break

        # Send user input to the server
        client_socket.send(message.encode())

    # Clean up the connection
    client_socket.close()


if __name__ == '__main__':
    start_client()

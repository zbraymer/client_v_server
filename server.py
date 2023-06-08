import socket
import time
from datetime import datetime
import threading


def send_time_to_client(client_socket):
    while True:
        # Get the current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send the current time to the client
        client_socket.send(current_time.encode())

        # Sleep for 1 minute
        time.sleep(60)


def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {server_address[0]}:{server_address[1]}')

        # Create a separate thread to send time to the client
        time_thread = threading.Thread(target=send_time_to_client, args=(client_socket,))
        time_thread.start()

        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode()

            # If the client has closed the connection, break the loop.
            if not data:
                break

            # If the client sends exit, break the loop.
            if data.lower() == 'exit':
                print('Client requested to exit. Closing the connection.')
                # Clean up the connection
                break

            # Convert the received data to uppercase
            uppercase_data = data.upper()

            # Send the echoed data back to the client
            client_socket.send(uppercase_data.encode())
            print(f'Received data from client: {uppercase_data}')

        # Clean up the connection
        client_socket.close()


if __name__ == '__main__':
    start_server()

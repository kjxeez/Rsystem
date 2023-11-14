# main.py
import socket
import threading

def client_program():
    # Create a TCP/IP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening.
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Send data.
        message = b'This is the message. It will be repeated.'
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response.
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))
    finally:
        print('closing socket')
        sock.close()

def server_program():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port.
    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections.
    sock.listen(1)

    while True:
        # Wait for a connection.
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it.
            while True:
                data = connection.recv(16)
                print('received {!r}'.format(data))
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break
        finally:
            # Clean up the connection.
            connection.close()

def main():
    # Создаем поток для сервера
    server_thread = threading.Thread(target=server_program)

    # Запускаем поток с сервером
    server_thread.start()

    # Запускаем клиента
    client_program()

if __name__ == "__main__":
    main()

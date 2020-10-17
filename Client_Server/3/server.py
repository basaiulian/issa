import socket
import sys


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def exercise1():
    data = connection.recv(256)
    my_print('[Server] Received "%s"' % data.decode())
    if data:
        my_print('[Server] Sending data back to the client')
        connection.sendall(data)
    else:
        my_print('[Server] No data to send')


def exercise2():
    data = connection.recv(256)
    my_print('[Server] Received:\n"%s"' % data.decode())
    if data:
        my_print('[Server] Sending data back to the client')
        connection.sendall(data)
    else:
        my_print('[Server] No data to send')


def exercise3():
    my_print('[Server] Sending request to', client_address)
    my_print('[Server] Type 0 for km or 1 for average speed ')
    request = input()
    connection.sendall(request.encode())
    my_print('[Server] Waiting for response... ')
    response = connection.recv(256)
    my_print('[Server] Response: %s' % response.decode())


# Creating TCP socket family:
# Address Format Internet
# Type: Socket Stream(sequenced, reliable, two-way connection-based byte streams over TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8000)
my_print('[Server] Starting up on %s port %s' % server_address)

sock.bind(server_address)

sock.listen(1)

while True:
    my_print('\n[Server] Waiting for a connection\n')

    # accept() returns an client connection and the address of the connected client
    connection, client_address = sock.accept()

    try:
        my_print('[Server] Connection from', client_address)

        my_print("[Server] Waiting for client's choice")
        choice = connection.recv(16).decode()
        if choice == "0":
            my_print('[Server] Received 0. Disconnecting...')
        elif choice == "1":
            my_print('[Server] Received 1. Running exercise 1.')
            exercise1()
        elif choice == "2":
            my_print('[Server] Received 2. Running exercise 2.')
            exercise2()
        elif choice == "3":
            my_print('[Server] Received 3. Running exercise 3.')
            exercise3()
        else:
            my_print('[Server] Invalid choice.')

    finally:
        connection.close()
        my_print('[Server] Connection ended')

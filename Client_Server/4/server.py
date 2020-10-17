import socket
import sys
import json


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


def exercise4():
    my_print("[Server] Geofence state [enabled | disabled]:")
    geofence_state = input()
    connection.sendall(geofence_state.encode())

    if geofence_state == "enabled":

        pair_a = {}
        pair_b = {}

        longitude_a = input("Pair A longitude: ")
        latitude_a = input("Pair A latitude: ")
        pair_a["longitude"] = longitude_a
        pair_a["latitude"] = latitude_a

        data_a_json = json.dumps(pair_a)
        connection.sendall(data_a_json.encode('utf-8'))

        longitude_b = input("Pair B longitude: ")
        latitude_b = input("Pair B latitude: ")
        pair_b["longitude"] = longitude_b
        pair_b["latitude"] = latitude_b

        data_b_json = json.dumps(pair_b)
        connection.sendall(data_b_json.encode('utf-8'))

        response = connection.recv(256)
        my_print("[Server] Geofence response: %s" % response.decode())

    elif geofence_state == "disabled":
        while True:
            my_print("[Server] Message to be sent [ send \"disconnect\" in order to close the connection ] : ")
            message = input()
            connection.sendall(message.encode('utf-8'))
            if message == "disconnect":
                break

    else:
        my_print("[Server] Invalid geofence state. Disconnecting.")


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
        elif choice == "4":
            my_print('[Server] Received 4. Running exercise 4.')
            exercise4()
        else:
            my_print('[Server] Invalid choice.')

    finally:
        connection.close()
        my_print('[Server] Connection ended')

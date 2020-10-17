import sys
import socket
import json


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def json_read_parse(file_path):
    # reading file
    f = open(file_path, "r")
    to_parse = f.read()

    # parsing json
    parsed = json.loads(to_parse)

    return parsed


def exercise1():
    simple_message = input("[Client] Send to server: ")
    message = simple_message
    expected_amount = len(message)

    my_print('[Client] Sending "%s"' % message)
    sock.sendall(message.encode('utf-8'))

    # Looking for the response
    received_amount = 0

    while received_amount < expected_amount:
        data = sock.recv(256)
        received_amount += len(data)
        my_print('[Client] Received "%s"' % data.decode())


def exercise2():
    json_message_1 = json_read_parse("C:/Users/Iulian/Desktop/Client_Server/Files/File1.txt")
    json_message_2 = json_read_parse("C:/Users/Iulian/Desktop/Client_Server/Files/File2.txt")
    json_message_to_send_1 = "From json(File 1): " + str(json_message_1["km"]) + " km and " + str(
        json_message_1["avgspeed"]) + " average speed."
    json_message_to_send_2 = "From json(File 2): " + str(json_message_2["latitude"]) + " latitude and " + str(
        json_message_2["longitude"]) + " longitude."
    message = json_message_to_send_1 + "\n" + json_message_to_send_2

    expected_amount = len(message)

    my_print('[Client] Sending "%s"' % message)
    sock.sendall(message.encode('utf-8'))

    received_amount = 0

    while received_amount < expected_amount:
        data = sock.recv(256)
        received_amount += len(data)
        my_print('[Client] Received "%s"' % data.decode())


# Creating TCP socket
# Family: Address Format Internet
# Type: Socket Stream(sequenced, reliable, two-way connection-based byte streams over TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting the socket to the port listened by the server
server_address = ('localhost', 8000)
my_print('[Client] Connecting to %s port %s' % server_address)
sock.connect(server_address)

user_input = input("[Client] What exercise do you want to test? Type 1, 2 or 0 (disconnect) \n")

if user_input == "1":
    sock.sendall(user_input.encode('utf-8'))
    exercise1()
elif user_input == "2":
    sock.sendall(user_input.encode('utf-8'))
    exercise2()
elif user_input == "0":
    sock.sendall(user_input.encode('utf-8'))
    my_print("[Client] Disconnecting...")
else:
    sock.sendall(user_input.encode('utf-8'))
    my_print('[Server] Invalid choice')
sock.close()

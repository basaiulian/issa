import sys
import socket
import json


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def json_read_parse(file_path):
    # Reading file
    f = open(file_path, "r")
    to_parse = f.read()

    # Parsing json
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


def exercise3():
    my_print("[Client] Waiting for server's request")
    json_message_3 = json_read_parse("C:/Users/Iulian/Desktop/Client_Server/Files/File1.txt")
    km = str(json_message_3["km"])
    avgspeed = str(json_message_3["avgspeed"])
    request = sock.recv(256)

    my_print("[Client] Received %s" % request.decode())
    my_print("[Client] Sending response")
    request = request.decode()
    if request == "1":
        sock.sendall(avgspeed.encode('utf-8'))
    elif request == "0":
        sock.sendall(km.encode('utf-8'))
    else:
        sock.sendall("[Client] Invalid command".encode('utf-8'))


def exercise4():
    state = "disabled"

    data_received = 0
    pair_a_longitude = 0
    pair_a_latitude = 0
    pair_b_longitude = 0
    pair_b_latitude = 0

    # do I need ? ^^

    json_message_4 = json_read_parse("C:/Users/Iulian/Desktop/Client_Server/Files/File2.txt")

    json_longitude = json_message_4["longitude"]
    json_latitude = json_message_4["latitude"]

    my_print("[Client] Initial longitude is %3f " % json_longitude)
    my_print("[Client] Initial latitude is %3f " % json_latitude)

    my_print("[Client] Waiting for state")
    state = sock.recv(256).decode()
    my_print("[Client] State received: %s" % state)

    if state == "enabled":
        received_pair = sock.recv(256)
        pair_a = json.loads(received_pair)
        pair_a_longitude = json.loads(pair_a["longitude"])
        pair_a_latitude = json.loads(pair_a["latitude"])

        my_print("[Client] Pair a = (%f, %f) " % (pair_a_longitude, pair_a_latitude))

        received_pair = sock.recv(256)
        pair_b = json.loads(received_pair)
        pair_b_longitude = json.loads(pair_b["longitude"])
        pair_b_latitude = json.loads(pair_b["latitude"])

        my_print("[Client] Pair b = (%f, %f) " % (pair_b_longitude, pair_b_latitude))

        # are initial coordinates set?
        if json_longitude == '' or json_latitude == '':
            my_print("[Client] Initial coordinates were not set.")
            response = "Initial coordinates were not set."
        else:
            if float(pair_a_longitude) < json_longitude < float(pair_b_longitude):
                if float(pair_a_latitude) < json_latitude < float(pair_b_latitude):
                    response = "Coordinates are in the rectangle."
                else:
                    response = "Coordinates are not in the rectangle. Wrong latitude."
            else:
                response = "Coordinates are in the rectangle. Wrong longitude."
        sock.sendall(response.encode('utf-8'))

    elif state == "disabled":
        while True:
            message = sock.recv(256).decode()
            my_print("[Client] Message received: %s" % message)
            if message == "disconnect":
                my_print("[Client] Disconnecting...")
                break
    else:
        my_print("[Client] Invalid geofence state.")


# Creating TCP socket
# Family: Address Format Internet T
# Type: Socket Stream(sequenced, reliable, two-way connection-based byte streams over TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting the socket to the port listened by the server
server_address = ('localhost', 8000)
my_print('[Client] Connecting to %s port %s' % server_address)
sock.connect(server_address)

user_input = input("[Client] What exercise do you want to test? Type 1, 2, 3, 4 or 0 (disconnect) \n")

if user_input == "1":
    sock.sendall(user_input.encode('utf-8'))
    exercise1()
elif user_input == "2":
    sock.sendall(user_input.encode('utf-8'))
    exercise2()
elif user_input == "3":
    sock.sendall(user_input.encode('utf-8'))
    exercise3()
elif user_input == "4":
    sock.sendall(user_input.encode('utf-8'))
    exercise4()
elif user_input == "0":
    sock.sendall(user_input.encode('utf-8'))
    my_print("[Client] Disconnecting...")
else:
    sock.sendall(user_input.encode('utf-8'))
    my_print('[Server] Invalid choice')
sock.close()

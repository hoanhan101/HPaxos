#!/usr/bin/env python3
"""
    server2.py - UDP server
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/16/2017
"""

import threading
import socket

UDP_ADDRESS = '127.0.0.1'
UDP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((UDP_ADDRESS, UDP_PORT))

clients = {}
PERMISSION_GRANTED_GROUP = []
ACCEPTED_MESSAGE_GROUP = []

class Server(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self.permitted_id = "1,A"
        self.accepted_id = "1,A"
        self.accepted_value = "Foo"

        self.numbers_of_clients = 1
        self.numbers_of_permission_granted = 0
        self.numbers_of_permission_denied = 0
        self.numbers_of_accepted_message = 0

    def send(self):
        while True:
            message = input("")

            if message == "q":
                for IP, port in clients.items():
                    s.sendto(message.encode(), (IP, port))
                    print("SENT {0} TO {1}".format(message, IP))
                    print("FINISHED SEND-THREAD")
                return

            # SEND ONE TO MYSELF
            s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
            print("SENT {0} TO {1}".format(message, UDP_ADDRESS))

            for IP, port in clients.items():
                s.sendto(message.encode(), (IP, port))
                print("SENT {0} TO {1}".format(message, IP))


    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            raw_data, addr = s.recvfrom(1024)
            raw_data = raw_data.decode()

            # update client's IP and Port
            clients[addr[0]] = addr[1]

            # print(clients)

            if raw_data == "q":
                print("FINISHED RECEIVE-THREAD")
                return

            try:
                data = split_string(raw_data, '_')

                # PERMISSION-REQUEST_5,A

                new_permitted_id = split_string(self.permitted_id, ',')
                new_data_id = split_string(data[1], ',')

                if data[0] == "PERMISSION-REQUEST":
                    print("RECEIVE PERMISSION REQUEST FROM {0}".format(addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        print("SUGGESTION ID {0} >= PERMITTED ID {1}".format(new_data_id, new_permitted_id))
                        self.permitted_id = data[1]

                        message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                        # SEND ONE TO MYSELF
                        s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                        print("SENT {0} TO {1}".format(message, UDP_PORT))

                        # SEND ONE TO EVERYBODY
                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))


                elif data[0] == "PERMISSION-GRANTED":
                    print("RECEIVE PERMISSION GRANTED FROM {0}".format(addr))

                    if (addr[0], addr[1]) not in PERMISSION_GRANTED_GROUP:
                        PERMISSION_GRANTED_GROUP.append((addr[0], addr[1]))

                        if len(PERMISSION_GRANTED_GROUP) >= int(self.numbers_of_clients / 2):
                            print("NUMBER OF PERMISSION GRANTED OVER CLIENTS {0}/{1}".format(
                                len(PERMISSION_GRANTED_GROUP), self.numbers_of_clients))

                            message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                            # SEND ONE TO MYSELF
                            s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                            print("SENT {0} TO {1}".format(message, UDP_PORT))

                            # SEND ONE TO EVERYBODY
                            for IP, port in clients.items():
                                s.sendto(message.encode(), (IP, port))
                                print("SENT {0} TO {1}".format(message, IP))
                                print(self.permitted_id, self.accepted_id, self.accepted_value)

                            print("SEND SUGGESTION TO ALL CLIENTS")
                        else:
                            print("DOESNT HAVE ENOUGH PERMISSION GRANTED VOTES FROM MAJORITY")
                    else:
                        print("ALREADY RECEIVE PERMISSION GRANTED FROM {0}".format((addr[0], addr[1])))


                elif data[0] == "SUGGESTION":
                    print("RECEIVE SUGGESTION FROM {0}".format(addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        print("SUGGESTION ID {0} >= PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                        self.permitted_id = data[1]
                        self.accepted_id = data[1]
                        self.accepted_value = data[2]

                        message = "ACCEPTED_{0}".format(self.permitted_id)

                        # SEND ONE TO MYSELF
                        s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                        print("SENT {0} TO {1}".format(message, UDP_PORT))

                        # SEND ONE TO EVERYBODY
                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                elif data[0] == "ACCEPTED":
                    print("RECEIVE ACCEPTED FROM {0}".format(addr))

                    if (addr[0], addr[1]) not in ACCEPTED_MESSAGE_GROUP:
                        ACCEPTED_MESSAGE_GROUP.append((addr[0], addr[1]))

                        if len(ACCEPTED_MESSAGE_GROUP) >= int(self.numbers_of_clients / 2):
                            self.accepted_id = data[1]
                            print("DONE")
                            print(self.permitted_id, self.accepted_id, self.accepted_value)
                        else:
                            print("DOESNT HAVE ENOUGH ACCEPTED MESSAGES FROM MAJORITY")
                    else:
                        print("ALREADY RECEIVE ACCEPTED MESSAGE FROM {0}".format((addr[0], addr[1])))

            except Exception as e:
                print("NO COMMAND FOUND : {0}".format(e))

    def run(self):
        if self.task == "SEND":
            self.send()
        else:
            self.receive()

def split_string(string, delimeter):
    string_array = string.split(delimeter)
    return string_array

def is_first_id_larger_and_equal(id_1, id_2):
    if int(id_1[0]) > int(id_2[0]):
        return True
    elif int(id_1[0]) == int(id_2[0]):
        if ord(id_1[1]) >= ord(id_2[1]):
            return True
    else:
        return False

if __name__ == '__main__':
    threading_lock = threading.Lock()
    threads = []

    SEND_THREAD = Server("SEND")
    RECEIVE_THREAD = Server("RECEIVE")

    SEND_THREAD.start()
    RECEIVE_THREAD.start()

    threads.append(SEND_THREAD)
    threads.append(RECEIVE_THREAD)

    for thread in threads:
        thread.join()

    print("FINISHED ALL THREADS")


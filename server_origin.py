#!/usr/bin/env python3
"""
    server2.py - UDP server
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/16/2017
"""

import threading
import socket

UDP_ADDRESS = '0.0.0.0'
UDP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((UDP_ADDRESS, UDP_PORT))

clients = {}

class Server(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self.permitted_id = "1,A"
        self.accepted_id = "1,A"
        self.accepted_value = "Foo"

    def send(self):
        while True:
            message = input("")

            if message == "q":
                for IP, port in clients.items():
                    s.sendto(message.encode(), (IP, port))
                    print("SENT {0} TO {1}".format(message, IP))
                    print("FINISHED SEND-THREAD")
                return

            for IP, port in clients.items():
                s.sendto(message.encode(), (IP, port))
                print("SENT {0} TO {1}".format(message, IP))


    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            raw_data, addr = s.recvfrom(1024)
            raw_data = raw_data.decode()
            clients[addr[0]] = addr[1]

            if raw_data == "q":
                print("FINISHED RECEIVE-THREAD")
                return

            try:
                data = split_string(raw_data, '_')

                # message = PERMISSION-REQUEST_5,A

                new_permitted_id = split_string(self.permitted_id, ',')
                new_data_id = split_string(data[1], ',')

                if data[0] == "PERMISSION-REQUEST":
                    print("RECEIVE PERMISSION REQUEST FROM {0}".format(addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        print("SUGGESTION ID {0} >= PERMITTED ID {1}".format(new_data_id, new_permitted_id))
                        self.permitted_id = data[1]

                        message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                elif data[0] == "SUGGESTION":
                    print("RECEIVE SUGGESTION FROM {0}".format(addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        print("SUGGESTION ID {0} >= PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                        self.permitted_id = data[1]
                        self.accepted_id = data[1]
                        self.accepted_value = data[2]

                        message = "ACCEPTED_{0}".format(self.permitted_id)

                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))


                elif data[0] == "PERMISSION-GRANTED":
                    print("RECEIVE PERMISSION GRANTED FROM {0}".format(addr))

                    self.permitted_id = data[1]
                    # NEED TODO SOMETHING WITH ACCEPTED ID AND VALUE
                    message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                    for IP, port in clients.items():
                        s.sendto(message.encode(), (IP, port))
                        print("SENT {0} TO {1}".format(message, IP))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)
                elif data[0] == "ACCEPTED":
                    print("RECEIVE ACCEPTED FROM {0}".format(addr))

                    self.accepted_id = data[1]
                    print("DONE")
                    print(self.permitted_id, self.accepted_id, self.accepted_value)
            except:
                print("NO COMMAND FOUND")

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


"""           
while True:
    raw_data, addr = s.recvfrom(1024)
    clients[addr[0]] = addr[1]

    raw_data = raw_data.decode()

    print("RECEIVE {0} FROM {1}".format(raw_data, addr[0]))

    data = raw_data.split(',')
    print(data)

    if data[0] == "PR":
        print("Received Permission Request")

    for IP, port in clients.items():
        s.sendto(raw_data.encode(), (IP, port))
        print("SENT {0} TO {1}".format(raw_data, IP))
"""
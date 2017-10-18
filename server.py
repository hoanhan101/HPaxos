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
        # self.permitted_id = "(1,\'A\')"
        # self.accepted_id = "(1,\'A\')"
        # self.accepted_value = "Foo"

    def send(self):
        while True:
            message = input(">> ")

            for IP, port in clients.items():
                s.sendto(message.encode(), (IP, port))
                print("SENT {0} TO {1}".format(message, IP))


    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            raw_data, addr = s.recvfrom(1024)
            raw_data = raw_data.decode()
            clients[addr[0]] = addr[1]

            try:
                data = split_string(raw_data, '_')

                # message = PERMISSION-REQUEST_16,B

                new_permitted_id = split_string(self.permitted_id, ',')
                new_data_id = split_string(data[1], ',')

                if data[0] == "PERMISSION-REQUEST":
                    if is_first_id_larger(new_data_id, new_permitted_id):
                        self.permitted_id = data[1]

                        message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))

                elif data[0] == "SUGGESTION":
                    if is_first_id_larger(new_data_id, new_permitted_id):
                        self.permitted_id = data[1]
                        self.accepted_id = data[1]
                        self.accepted_value = data[2]

                        message = "ACCEPTED_{0}".format(self.permitted_id)

                        for IP, port in clients.items():
                            s.sendto(message.encode(), (IP, port))
                            print("SENT {0} TO {1}".format(message, IP))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)

                elif data[0] == "PERMISSION-GRANTED":
                    self.permitted_id = data[1]
                    # NEED TODO SOMETHING WITH ACCEPTED ID AND VALUE
                    message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                    for IP, port in clients.items():
                        s.sendto(message.encode(), (IP, port))
                        print("SENT {0} TO {1}".format(message, IP))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)
                elif data[0] == "ACCEPTED":
                    self.accepted_id = data[1]
                    print("DONE")
                    print(self.permitted_id, self.accepted_id, self.accepted_value)
            except:
                print("NO COMMAND FOUND")


                # print("RECEIVE {0} FROM {1}".format(raw_data, addr[0]))

    def run(self):
        if self.task == "SEND":
            self.send()
        else:
            self.receive()
        # print("FINISHED {0}_THREAD".format(self.task))


def split_string(string, delimeter):
    string_array = string.split(delimeter)
    return string_array

def is_first_id_larger(id_1, id_2):
    if int(id_1[0]) >= int(id_2[0]) and ord(id_1[1]) >= ord(id_2[1]):
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

    # print("DONE")


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
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
        self.permitted_id = "(1,\'A\')"
        self.accepted_id = "(1,\'A\')"
        self.accepted_value = "Foo"

    def send(self):
        while True:
            message = input(">> ")

            for IP, port in clients.items():
                s.sendto(message.encode(), (IP, port))
                print("SENT {0} TO {1}".format(message, IP))


    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode()
            clients[addr[0]] = addr[1]

            new_data = split_string(data, '_')
            if new_data[0] == "PERMISSION-REQUEST":
                if self.permitted_id < new_data[1]:
                    self.permitted_id = new_data[1]

                    message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                    for IP, port in clients.items():
                        s.sendto(message.encode(), (IP, port))
                        print("SENT {0} TO {1}".format(message, IP))

            elif new_data[0] == "SUGGESTION":
                if self.permitted_id <= new_data[1]:
                    self.permitted_id = new_data[1]
                    self.accepted_id = new_data[1]
                    self.accepted_value = new_data[2]

                    message = "ACCEPTED_{0}".format(self.permitted_id)

                    for IP, port in clients.items():
                        s.sendto(message.encode(), (IP, port))
                        print("SENT {0} TO {1}".format(message, IP))
                    print(self.permitted_id, self.accepted_id, self.accepted_value)

            elif new_data[0] == "PERMISSION-GRANTED":
                self.permitted_id = new_data[1]
                # NEED TODO SOMETHING WITH ACCEPTED ID AND VALUE
                message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                for IP, port in clients.items():
                    s.sendto(message.encode(), (IP, port))
                    print("SENT {0} TO {1}".format(message, IP))
                    print(self.permitted_id, self.accepted_id, self.accepted_value)
            elif new_data[0] == "ACCEPTED":
                self.accepted_id = new_data[1]
                print("DONE")
                print(self.permitted_id, self.accepted_id, self.accepted_value)



                # print("RECEIVE {0} FROM {1}".format(data, addr[0]))

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
    data, addr = s.recvfrom(1024)
    clients[addr[0]] = addr[1]

    data = data.decode()

    print("RECEIVE {0} FROM {1}".format(data, addr[0]))

    new_data = data.split(',')
    print(new_data)

    if new_data[0] == "PR":
        print("Received Permission Request")

    for IP, port in clients.items():
        s.sendto(data.encode(), (IP, port))
        print("SENT {0} TO {1}".format(data, IP))
"""
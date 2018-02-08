#!/usr/bin/env python3
"""
    client_multi_thread.py - UDP client multi-thread
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/16/2017
"""

import threading
import socket

UDP_ADDRESS = '127.0.0.1'
UDP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clients = {}

class Client(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self.permitted_id = "2,E"
        self.accepted_id = "2,E"
        self.accepted_value = "Bar"

    def send(self):
        while True:
            message = input("")

            if message == "q":
                s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                print("FINISHED SEND-THREAD")
                return

            s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
            print("SENT {0} TO {1}".format(message, UDP_ADDRESS))

    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            raw_data, addr = s.recvfrom(1024)
            raw_data = raw_data.decode()

            if raw_data == "q":
                print("FINISHED RECEIVE-THREAD")
                return

            try:
                data = split_string(raw_data, '_')

                new_permitted_id = split_string(self.permitted_id, ',')
                new_data_id = split_string(data[1], ',')

                if data[0] == "PERMISSION-REQUEST":
                    print("RECEIVE PERMISSION REQUEST {0} FROM {1}".format(new_data_id, addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        self.permitted_id = data[1]

                        message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                        s.sendto(message.encode(), addr)
                        print("SENT {0} TO {1}".format(message, addr))
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                        new_suggestion_id = "{0},{1}".format(int(new_permitted_id[0]) + 1, new_permitted_id[1])

                        message = "PERMISSION-REQUEST_{0}".format(new_suggestion_id)

                        s.sendto(message.encode(), addr)
                        print("SENT {0} TO {1}".format(message, addr))

                elif data[0] == "PERMISSION-GRANTED":
                    print("RECEIVE PERMISSION GRANTED FROM {0}".format(addr))

                    self.permitted_id = data[1]

                    message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                    s.sendto(message.encode(), addr)
                    print("SENT {0} TO {1}".format(message, addr))

                elif data[0] == "SUGGESTION":
                    print("RECEIVE SUGGESTION FROM {0}".format(addr))

                    if is_first_id_larger_and_equal(new_data_id, new_permitted_id):
                        print("{0} > {1}".format(new_data_id, new_permitted_id))

                        self.permitted_id = data[1]
                        self.accepted_id = data[1]
                        self.accepted_value = data[2]

                        message = "ACCEPTED_{0}".format(self.permitted_id)

                        s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                        print(self.permitted_id, self.accepted_id, self.accepted_value)
                    else:
                        print("SUGGESTION ID {0} < PERMITTED ID {1}".format(new_data_id, new_permitted_id))

                        new_suggestion_id = "{0},{1}".format(int(new_permitted_id[0]) + 1, new_permitted_id[1])

                        message = "PERMISSION-REQUEST_{0}".format(new_suggestion_id)

                        s.sendto(message.encode(), addr)
                        print("SENT {0} TO {1}".format(message, addr))


                elif data[0] == "ACCEPTED":
                    print("RECEIVE ACCEPTED FROM {0}".format(addr))

                    self.accepted_id = data[1]
                    print("DONE")
                    print(self.permitted_id, self.accepted_id, self.accepted_value)

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

    SEND_THREAD = Client("SEND")
    RECEIVE_THREAD = Client("RECEIVE")

    SEND_THREAD.start()
    RECEIVE_THREAD.start()

    threads.append(SEND_THREAD)
    threads.append(RECEIVE_THREAD)

    for thread in threads:
        thread.join()

    print("FINISHED ALL THREADS")
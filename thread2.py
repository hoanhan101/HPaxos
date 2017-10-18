#!/usr/bin/env python3
"""
    thread2.py - First example of using simple threading using the Thread object.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 9/24/2017
"""

import threading
import time


class TimeThread(threading.Thread):
    """
    Class that encapsulates a thread that prints the time a given number of times given a delay.
    """
    def __init__(self, thread_id, name, counter, delay):
        """
        Initialize the TimeThread.
        :param thread_id: The ID of the thread (unused)
        :param name: A friendly name for the thread.
        :param counter: How many times to print the time message.
        :param delay: How long to wait between printing messages.
        :return: None.
        """
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        self.delay = delay

    def print_time(self):
        """
        Print the thread name and current time 5 times, waiting for the delay specified between iterations.
        :return: None.
        """
        while self.counter:
            time.sleep(self.delay)
            print("{0} {1} ".format(self.name, time.ctime()))
            self.counter -= 1

    def run(self):
        """
        Runs the thread (called when the thread is start()ed.)
        :return: None.
        """
        print('Starting {0}'.format(self.name))
        self.print_time()
        print('Finishing {0}'.format(self.name))


thread_lock = threading.Lock()
threads = []

thread_1 = TimeThread(1, "thread_1", 1, 1)
thread_2 = TimeThread(2, "thread_2", 1, 2)

thread_1.start()
thread_2.start()

threads.append(thread_1)
threads.append(thread_2)

for thread in threads:
	thread.join()

print('DONE')

#!/usr/bin/env python3
"""
    message.py - Test different kinds of messages
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/16/17
"""

class Message(object):
    def permission_request(self):
        print("permission request")
    def permission_granted(self):
        print("permission granted")
    def suggestion(self):
        print("suggestion")
    def accepted(self):
        print("accepted")
    def permission_request_denied(self):
        print("permission request denied")
    def suggestion_denied(self):
        print("suggestion denied")

if __name__ == '__main__':
    messenger = Message()

    agree_on_permission_request = True
    agree_on_suggestion = True

    while True:
        message = input("message = ")

        if message == "permission request":
            if agree_on_permission_request == True:
                messenger.permission_granted()
            else:
                messenger.permission_request_denied()
        elif message == "permission request denied":
            messenger.permission_request()
        elif message == "permission granted":
            agree_on_permission_request = True
            messenger.suggestion()
        elif message == "suggestion":
            if agree_on_suggestion == True:
                messenger.accepted()
            else:
                messenger.suggestion_denied()
        elif message == "suggestion denied":
            messenger.permission_request()
        elif message == "accepted":
            print("reach consensus")
            break
        else:
            print("no message found")
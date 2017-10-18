#!/usr/bin/env python3
"""
    paxos_case_2.py - Paxos Case 2 Implementation
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/10/17
"""

import collections

SuggestionID = collections.namedtuple('SuggestionID', ['number', 'uid'])

class Peer(object):
    def __int__(self, name, permitted_id, accepted_id, accepted_value):
        self.name = name
        self.permitted_id = permitted_id
        self.accepted_id = accepted_id
        self.accepted_value = accepted_value
        self.permitted_id_from_suggestion_denied = None
        self.new_suggestion_id = None

    def send_suggestion(self, receiver, suggestion_id, value):
        if self.new_suggestion_id is not None:
            self.accepted_id = self.new_suggestion_id

        print("{0} SEND SUGGESTION ID: {1} VALUE: {2} TO {3}".format(self.name, suggestion_id, value, receiver.name))

    def receive_suggestion(self, sender, suggestion_id, value):
        if suggestion_id < self.permitted_id:
            print("BECAUSE {0} SUGGESTION ID: {1} < {2} PERMITTED ID: {3}".format(sender.name, suggestion_id, self.name, self.permitted_id))
            return False
        else:
            self.accepted_id = suggestion_id
            self.accepted_value = value
            print("{0} RECEIVE SUGGESTION ID: {1} VALUE: {2} FROM {3}".format(self.name, suggestion_id, value, sender.name))
            print("{0} PREPARE TO SEND ACCEPTED MESSAGE TO {1}".format(self.name, sender.name))

    def send_accepted_message(self, receiver, accepted_id):
        print("{0} SEND ACCEPTED MESSAGE WITH ACCEPTED ID: {1} TO {2}".format(self.name, self.accepted_id, receiver.name))

    def send_suggestion_denied(self, receiver, permitted_id):
        print("{0} SEND PERMISSION DENIED {1} TO {2}".format(self.name, self.permitted_id, receiver.name))

    def receive_suggestion_denied(self, sender, permitted_id):
        self.permitted_id_from_suggestion_denied = permitted_id
        print("{0} RECEIVE PERMISSION DENIED {1} FROM {2}".format(self.name, self.permitted_id_from_suggestion_denied, sender.name))

    def send_permission_request(self, receiver):
        self.new_suggestion_id = SuggestionID(self.permitted_id_from_suggestion_denied.number + 1, self.accepted_id.uid)
        self.permitted_id = self.new_suggestion_id
        print("{0} MAKE NEW SUGGESTION ID: {1}".format(self.name, self.new_suggestion_id))
        print("{0} SEND NEW SUGGESTION ID: {1} TO {2}".format(self.name, self.new_suggestion_id, receiver.name))

    def receive_permission_request(self, sender, suggestion_id):
        if suggestion_id > self.permitted_id:
            self.permitted_id = suggestion_id
            print("NOW {0} SUGGESTION ID > {1} PERMITTED ID".format(sender.name, self.name))
            print("{0} PREPARE TO SEND PERMISSION GRANTED TO {1}".format(self.name, sender.name))
        else:
            return False

    def send_permission_granted(self, receiver, permitted_id, accepted_id, accepted_value):
        print("{0} SEND PERMITED ID: {1}, ACCEPTED ID: {2}, ACCEPTED VALUE: {3} TO {4}".format(self.name, self.permitted_id, self.accepted_id, self.accepted_value, receiver.name))

    def receive_permission_granted(self, sender, permitted_id, accepted_id, accepted_value):
        print("{0} RECEIVE PERMITTED ID: {1}, ACCEPTED ID: {2}, ACCEPTED VALUE: {3} FROM {4}".format(self.name, sender.permitted_id, sender.accepted_id, sender.accepted_value, sender.name))



def print_list_of_peers(peers):
    for peer in peers:
        print("{0}: PERMITTED ID: {1}, ACCEPTED ID: {2}, ACCEPTED VALUE: {3}".format(peer.name, peer.permitted_id,
                                                                                     peer.accepted_id,
                                                                                     peer.accepted_value))


if __name__ == '__main__':

    # Peer A is Suggester

    peer_A = Peer()
    peer_A.name = "PEER A"
    peer_A.permitted_id = SuggestionID(1, 'A')
    peer_A.accepted_id = SuggestionID(1, 'A')
    peer_A.accepted_value = 'Foo'
    peer_A.permitted_id_from_suggestion_denied = None
    peer_A.new_suggestion_id = None

    peer_B = Peer()
    peer_B.name = "PEER B"
    peer_B.permitted_id = SuggestionID(1, 'A')
    peer_B.accepted_id = SuggestionID(1, 'A')
    peer_B.accepted_value = 'Foo'
    peer_B.permitted_id_from_suggestion_denied = None
    peer_B.new_suggestion_id = None

    peer_C = Peer()
    peer_C.name = "PEER C"
    peer_C.permitted_id = SuggestionID(2, 'E')
    peer_C.accepted_id = None
    peer_C.accepted_value = None
    peer_C.permitted_id_from_suggestion_denied = None
    peer_C.new_suggestion_id = None

    # Add all Peers to list

    peers = []
    peers.append(peer_A)
    peers.append(peer_B)
    peers.append(peer_C)


    # Starting Case 2

    print("BEFORE:")
    print_list_of_peers(peers)

    print("")
    print("PROCESS:")

    print("1")
    print_list_of_peers(peers)
    print("")

    peer_A.send_suggestion(peer_C, peer_A.accepted_id, peer_A.accepted_value)

    print("")
    print("2")
    print_list_of_peers(peers)
    print("")

    if peer_C.receive_suggestion(peer_A, peer_A.accepted_id, peer_A.accepted_value) == False:
        peer_C.send_suggestion_denied(peer_A, peer_C.permitted_id)

    peer_A.receive_suggestion_denied(peer_C, peer_C.permitted_id)

    print("")
    print("3")
    print_list_of_peers(peers)
    print("")

    peer_A.send_permission_request(peer_C)
    peer_A.send_permission_request(peer_B)

    peer_C.receive_permission_request(peer_A, peer_A.new_suggestion_id)
    peer_B.receive_permission_request(peer_A, peer_A.new_suggestion_id)

    print("")
    print("4")
    print_list_of_peers(peers)
    print("")

    peer_C.send_permission_granted(peer_A, peer_C.permitted_id, peer_C.accepted_id, peer_C.accepted_value)
    peer_B.send_permission_granted(peer_A, peer_B.permitted_id, peer_B.accepted_id, peer_B.accepted_value)

    peer_A.receive_permission_granted(peer_C, peer_C.permitted_id, peer_C.accepted_id, peer_C.accepted_value)
    peer_A.receive_permission_granted(peer_B, peer_B.permitted_id, peer_B.accepted_id, peer_B.accepted_value)


    print("")
    print("5")
    print_list_of_peers(peers)
    print("")

    peer_A.send_suggestion(peer_C, peer_A.new_suggestion_id, peer_A.accepted_value)
    peer_A.send_suggestion(peer_B, peer_B.new_suggestion_id, peer_B.accepted_value)

    peer_C.receive_suggestion(peer_A, peer_A.new_suggestion_id, peer_A.accepted_value)
    peer_B.receive_suggestion(peer_A, peer_A.new_suggestion_id, peer_A.accepted_value)

    print("")
    print("6")
    print_list_of_peers(peers)
    print("")

    peer_C.send_accepted_message(peer_A, peer_C.accepted_id)
    peer_B.send_accepted_message(peer_A, peer_B.accepted_id)

    print("")
    print("AFTER:")
    print_list_of_peers(peers)

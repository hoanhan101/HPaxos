#!/usr/bin/env python3
"""
    paxos_components.py - Paxos Components
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/10/17
"""

import collections

SuggestionID = collections.namedtuple('SuggestionID', ['number', 'uid'])

class Message(object):
    
    def permission_request(self, suggestion_id):
#        print("PERMISSION REQUEST")
        return True

    def permission_granted(self, suggestion_id, accepted_id, accepted_value):
#        print("PERMISSION GRANTED")
        return True

    def suggestion(self, suggestion_id, suggestion_value):
#        print("SUGGESTION")
        return True

    def accepted(self, suggestion_id, accepted_value):
#        print("ACCEPTED")
        return True

class Suggester(object):

    message = Message()

    NUMBERS_OF_PEERS = None
    uid = None
    suggestion_id = None
    accepted_id = None
    accepted_value = None
    suggestion_counter = 1

    # Create a set of all Permission Granted that Suggester have received
    received_permissions_granted_list = list()

    # Send Permission Request to all Voters
    def send_permission_request(self):
        # Create a unique Suggestion ID
        # Increase suggestion counter to ensure correctness
        self.suggestion_id = SuggestionID(self.suggestion_counter, self.uid)
        self.suggestion_counter += 1
        self.message.permission_request(self.suggestion_id)
        print("SUGGESTER    ACCEPTED_ID: {0}    ACCEPTED_VALUE: {1}".format(self.accepted_id, self.accepted_value))
        print(">> SENT PERMISSION REQUEST     {0}".format(self.suggestion_id))

    # Receive Permission Granted from Voter
    def receive_permission_granted(self, suggestion_id, accepted_id, accepted_value):
        # If Suggestion ID doesn't match or Suggester have received Permission Granted from this Voter, return
        if suggestion_id != self.suggestion_id or suggestion_id.uid in self.received_permissions_granted_list:
            return

        self.received_permissions_granted_list.append(suggestion_id.uid)
        
        # If Voter's Last Accepted ID is newer than Suggester's Last Accepted ID, update Suggester's Last Accepted ID
        if accepted_id > self.accepted_id:
            self.accepted_id = accepted_id
            
            # If Voter's Last Accepted Value is NOT NULL, update Suggester's Last Accepted Value
            if accepted_value is not None:
                self.accepted_value = accepted_value
        
        # If Suggester have received Permision Granted from majority of Voters, send Suggestion messages to all Voters
        if len(self.received_permissions_granted_list) >= int(self.NUMBERS_OF_PEERS / 2):
            if self.accepted_value is not None:
                self.message.suggestion(self.suggestion_id, self.accepted_value)
                print("SUGGESTER    ACCEPTED_ID: {0}    ACCEPTED_VALUE: {1}".format(self.accepted_id, self.accepted_value))
                print(">> SENT SUGGESTION     {0} {1}".format(self.suggestion_id, self.accepted_value))

class Voter(object):
    
    message = Message()

    permitted_id = None
    accepted_id = None
    accepted_value = None

    # Receive Permission Request from Suggester
    # If Suggestion ID is newer than Permited ID, update Permitted ID and send Permission Granted to Suggestor
    def receive_permission_request(self, suggestion_id):
        # Duplicate Permission Request
        if suggestion_id >= self.permitted_id:
            self.permitted_id = suggestion_id
            self.message.permission_granted(suggestion_id, self.accepted_id, self.accepted_value)
            print("VOTER    PERMITEED_ID: {0}   ACCEPTED_ID: {1}    ACCEPTED_VALUE: {2}".format(self.permitted_id,self.accepted_id, self.accepted_value))
            print(">> SENT PERMISSION GRANTED     {0}".format(self.permitted_id))

        else:
            print("SUGGESTER {0} < VOTER {1}".format(suggestion_id, self.permitted_id))

    # Receive Suggestion from Suggester
    def receive_suggestion(self, suggestion_id, suggestion_value):
        # If Suggestion ID is newer than Permitted ID, update Permitted ID, Accepted ID, Accepted Value
        # and send Accepted message to all Arbiters
        if suggestion_id >= self.permitted_id:
            self.permitted_id = suggestion_id
            self.accepted_id = suggestion_id
            self.accepted_value = suggestion_value

            self.message.accepted(suggestion_id, self.accepted_value)
            print("VOTER    PERMITEED_ID: {0}   ACCEPTED_ID: {1}    ACCEPTED_VALUE: {2}".format(self.permitted_id,self.accepted_id, self.accepted_value))
            print(">> SENT ACCEPTED MESSAGE   {0} {1}".format(suggestion_id, self.accepted_value))

        else:
            print("{0} < {1}".format(suggestion_id, self.permitted_id))

class Arbiter(object):

    suggestions = list()
    accepted_id = None
    accepted_value = None

    # Receive Accepted message from Voters
    def receive_accepted_message(self, suggestion_id, accepted_value):
        self.suggestions.append(suggestion_id)
        if suggestion_id >= max(self.suggestions):
            self.accepted_id = suggestion_id
            self.accepted_value = accepted_value
            print("ARBITER      ACCEPTED_ID: {0}    ACCEPTED_VALUE: {1}".format(self.accepted_id, self.accepted_value))
            print("CONSENSUS")

if __name__ == '__main__':

    MAX_NUMBER_OF_PEERS = 1

    suggester_1 = Suggester()
    suggester_1.NUMBERS_OF_PEERS = MAX_NUMBER_OF_PEERS
    suggester_1.uid = 'A'
    suggester_1.accepted_id = SuggestionID(1, 'A')
    suggester_1.accepted_value = 'Foo'

    voter_1 = Voter()
    voter_1.permitted_id = SuggestionID(2, 'A')
    voter_1.accepted_id = SuggestionID(1, 'A')
    voter_1.accepted_value = 'Foo'

    suggester_1.send_permission_request() # SuggestionID = (1, A)
    voter_1.receive_permission_request(suggester_1.suggestion_id)


"""
    suggester_1.send_permission_request()
    suggester_1.send_permission_request()
    suggester_1.send_permission_request()

    # SUGGESTER    ACCEPTED_ID: SuggestionID(number=1, uid='A')    ACCEPTED_VALUE: Foo
    # >> SENT PERMISSION REQUEST     SuggestionID(number=3, uid='A')

    voter_1 = Voter()
    voter_1.permitted_id = SuggestionID(1, 'A')
    voter_1.accepted_id = SuggestionID(1, 'A')
    voter_1.accepted_value = 'Bar'

    voter_2 = Voter()
    voter_2.permitted_id = SuggestionID(5, 'A')
    voter_2.accepted_id = SuggestionID(5, 'A')
    voter_2.accepted_value = 'Bar'

    voter_1.receive_permission_request(suggester_1.suggestion_id)

    suggester_1.receive_permission_granted(voter_1.permitted_id, voter_1.accepted_id, voter_1.accepted_value)

    voter_1.receive_suggestion(suggester_1.suggestion_id, suggester_1.accepted_value)

    arbiter_1 = Arbiter()
    arbiter_1.accepted_id = SuggestionID(1, 'A')
    arbiter_1.accepted_value = 'Bar'

    arbiter_1.receive_accepted_message(voter_1.accepted_id, voter_1.accepted_value)
"""

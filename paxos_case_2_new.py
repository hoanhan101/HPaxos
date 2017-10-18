#!/usr/bin/env python3
"""
    paxos_case_2.py - Paxos Case 2 Implementation
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/10/17
"""

import collections

SuggestionID = collections.namedtuple('SuggestionID', ['number', 'uid'])

"""
    If a Peer receive SUGGESTION:
        if that corresponding SUGGESTION ID IS LESS THAN a Peer's PERMITTED ID
            deny it
                send back its Permitted ID
                
            accept it
                update PERMITTED ID
                send back 

    If a Peer receive SUGGESTION DENIED 
    
    a Peer can have two threads
        one to send
            send permission request
            send permission request denied
            
            send permission granted
            
            send suggestion
            send suggestion denied
            
            send accepted message
        one to receive
            receive permission request
                if agree, send permission granted
                if not, send permission request denied
                
            receive permission request denied
                send permission request again
            
            receive permission granted
                send suggestion
                
            receive suggestion
                if agree, send accepted message,
                if not, send suggestion denied
                
            receive suggestion denied
                send permission request again

            receive accepted message
                done
        


"""
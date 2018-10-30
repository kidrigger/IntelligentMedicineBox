#!/bin/python3

"""
Event Queue
Recieves events from Subjects and notifies
"""

class Event:
    etype = 'none'
    data = {}

    def __init__(self, etype, data):
        self.etype = etype
        self.data = data

class EventQueue:
    _event_queue = {}
    _event_types = []
    _event_listeners = {}
    
    def __init__(self,event_types = []):
        self._event_types = event_types[:]
        self._event_queue = {}
        self._event_listeners = {}
        for etype in event_types:
            self._event_listeners[etype] = []
            self._event_queue[etype] = []

    def new_event(self, event):
        print('new_event', event.etype)
        self._event_queue[event.etype].append(event)

    def update(self):
        for etype in self._event_types:
            for listener in self._event_listeners[etype]:
                for event in self._event_queue[etype]:
                    listener.notify(event)
            self._event_queue[etype] = []
    
    def register(self, listener, listen_etypes = []):
        for etype in listen_etypes:
            self._event_listeners[etype].append(listener)
    


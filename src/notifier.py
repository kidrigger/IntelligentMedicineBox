#!/bin/python3

"""
Notifier
Gathers notifications from EventQueue and sends them to PrescriptionManager.
"""

class Notifier:
    _external_communication_sys

    def __init__(self, external_communication_sys=None):
        _external_communication_sys = external_communication_sys

    def notify(event):
        if event.etype == 'alert' :
            print('Alert: ' + event.data)
        else if event.etype == 'print' :
            print('Print: ' + event.data)
        else if event.etype == 'update' :
            print('Update: ' + event.data)
        else:
            print('Unknown event: ' + event.data)

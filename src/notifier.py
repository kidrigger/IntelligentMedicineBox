#!/bin/python3
from event_queue import EventQueue
import firebase_admin
from firebase_admin import credentials, db

"""
Notifier
Gathers notifications from EventQueue and sends them to PrescriptionManager.
"""

class Notifier:
    _ref = None
    _notification_ref= None
    _prescription_ref= None

    def __init__(self, event_queue, patient_name):
        event_queue.register(self, ['alert', 'presc_man'])
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('./access_key/intelligent-medicine-box-firebase-adminsdk-iio70-6832e102bb.json')

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://intelligent-medicine-box.firebaseio.com/'
        })

        # As an admin, the app has access to read and write all data, regardless of Security Rules
        self._ref = db.reference('/patients/')
        self._prescription_ref = self._ref.child(patient_name + '/prescriptions/')
        self._notification_ref = self._ref.child(patient_name + '/notifications/')
        print(self._ref.get())

    def _send_alert(self, alert_event):
        print('sending alert', alert_event)
        self._notification_ref.push().set(alert_event.data)

    def _send_pres(self, presc):
        print('sending prescription', presc)
        self._prescription_ref.child('pres'+presc['id']).set(presc)

    def notify(self, event):
        #print(event.data, 'in notifier')
        if event.etype == 'alert' :
            self._send_alert(event)
        elif event.etype == 'presc_man':
            self._send_pres(event.data['prescription'])
        #    print('Alert: ' + event.data)
        #else if event.etype == 'print' :
        #    print('Print: ' + event.data)
        #else if event.etype == 'update' :
        #    print('Update: ' + event.data)
        #else:
        #    print('Unknown event: ' + event.data)


#!/bin/python3
from event_queue import EventQueue
#import firebase_admin
#from firebase_admin import credentials, db
import pyrebase

"""
Notifier
Gathers notifications from EventQueue and sends them to PrescriptionManager.
"""


class Notifier:
    #_ref = None
    #_notification_ref= None
    #_prescription_ref= None
    _user = None
    _db = None
    _patient_id = None

    def __init__(self, event_queue):
        event_queue.register(self, ['alert', 'presc_man'])

    def pyrebase_init(self, email, password):

        # Fetch the service account key JSON file contents

        # As an admin, the app has access to read and write all data, regardless of Security Rules
        config = {
            "apiKey": "AIzaSyDt-RK1Njxn_aqMOcl0ngKv9mTp886Ebh4",
            "authDomain": "intelligent-medicine-box.firebaseapp.com",
            "databaseURL": "https://intelligent-medicine-box.firebaseio.com",
            "storageBucket": "intelligent-medicine-box.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        self._db = firebase.database()

        # authenticate a user
        if email is None or password is None:
            print('email or password is None in notifier')
            assert(False)
        # login the user.
        try:
            self._user = auth.sign_in_with_email_and_password(email, password)
        except Exception:
            print("Wrong login or password.")
            return False
        # print(user)

        self._patient_id = self._user['localId']
        # print(self._ref.get())

        print("Login successful.")
        return True

    def _send_alert(self, alert_event):
        print('sending alert', alert_event.data)
        self._db.child('/patients/' + self._patient_id +
                       '/notifications/').push(alert_event.data, self._user['idToken'])

    def _send_pres(self, presc):
        print('sending prescription', presc)
        self._db.child('/patients/' + self._patient_id + '/prescriptions/').child(
            'pres'+presc['id']).set(presc, self._user['idToken'])

    def notify(self, event):
        #print(event.data, 'in notifier')
        if event.etype == 'alert':
            self._send_alert(event)
        elif event.etype == 'presc_man':
            self._send_pres(event.data['prescription'])
        #    print('Alert: ' + event.data)
        # else if event.etype == 'print' :
        #    print('Print: ' + event.data)
        # else if event.etype == 'update' :
        #    print('Update: ' + event.data)
        # else:
        #    print('Unknown event: ' + event.data)

#!/bin/python3
from event_queue import *
import constants

class PrescriptionManager:

    _evq = None
    _prescriptions = None
    _slots = []
    _current_slot = 0

    def __init__(self, evq):
        self._prescriptions = []
        self._evq = evq
        self._slots = constants.slots
        self._current_slot = 0
        self._evq.register(self, ['presc_man', 'timeslot'])

    def new_prescription(self, prescription):
        slotarray = [0]*8
        for meds in prescription['medicines'].items():
            for i,d in enumerate(meds[1]):
                slotarray[i] += d
        prescription['_slotarray_'] = slotarray
        self._prescriptions.append(prescription)
    
    def delete_prescription(self, prescription_id):
        for presc in self._prescriptions:
            if presc['id'] == prescription_id:
                self._prescriptions.remove(presc)       # Changed here.
                break
    
    def update_prescription(self, prescription):
        self.delete_prescription(prescription['id'])    # Changed here.
        self.new_prescription(prescription)
    
    def get_prescribed_medicine(self, timeslot):
        timeslot_medicines = {}
        for prescription in self._prescriptions:
            print(prescription)
            for medicine in prescription['medicines']:
                slot_medcount = prescription['medicines'][medicine][timeslot] 
                if slot_medcount > 0:
                    timeslot_medicines[medicine] = slot_medcount
        return timeslot_medicines

    def get_next_slot(self, timeslot):
        for i in range(timeslot+1, 8):
            for presc in self._prescriptions:
                if presc['_slotarray_'][i] > 0:
                    return i
        for i in range(0, timeslot+1):
            for presc in self._prescriptions:
                if presc['_slotarray_'][i] > 0:
                    return i

    def notify(self, event):
        if event.etype == 'timeslot':
            self._current_slot += event.data['timeinc']
            next_slot = self.get_next_slot(self._current_slot)
            self.notify_user(self.get_prescribed_medicine(self._current_slot))
            self._evq.new_event(Event('timer', {'time':self._slots[next_slot][0],'etype':'timeslot', 'timeinc':next_slot-self._current_slot}))
        elif event.etype == 'presc_man':
            if event.data['type'] == 'new':
                self.new_prescription(event.data['prescription'])
            elif event.data['type'] == 'update':
                self.update_prescription(event.data['prescription'])
            elif event.data['type'] == 'delete':
                self.delete_prescription(event.data['prescription_id'])
    
    def notify_user(self, what):
        self._evq.new_event(Event('message',{'data': what}))


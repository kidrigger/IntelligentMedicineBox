#!/bin/python3
from event_queue import *
import constants
from timer import get_current_time
from copy import deepcopy

class PrescriptionManager:

    _evq = None
    _prescriptions = None
    _slots = []
    _current_slot = 0

    def __init__(self, evq, slot_num=None):
        if slot_num is None:
            slot_num = constants.get_slot_num(get_current_time())
        self._current_slot = slot_num
        self._prescriptions = []
        self._evq = evq
        self._slots = constants.slots
        self._evq.register(self, ['presc_man', 'timeslot', 'slot_begin'])
        #print(slot_num)
        self._set_next_slot_alarm(slot_num)

    def _set_next_slot_alarm(self, slot_num):
        #print(slot_num)
        next_slot_index = (slot_num+1)%8
        #print(next_slot_index)
        next_slot_time = constants.get_slot_time(next_slot_index)
        next_slot_begin_event = Event('timer', {'time':next_slot_time[0], 'etype':'slot_begin', 'timetuple':next_slot_time} )
        self._evq.new_event(next_slot_begin_event)

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
     
    def _send_med_reminder(self, timeslot):
        meds_prescribed = self.get_prescribed_medicine(timeslot)
        for key,value in meds_prescribed.items():
             message="You have to take "+str(value)+" pill of "+str(key)+" in this slot" 	        
             #print (message)
             self.notify_user({'msg':message, 'type':'reminder'})

    def notify(self, event):
        if event.etype == 'presc_man':
            event_data = deepcopy(event.data)
            #print(event_data)
            if event.data['type'] == 'new':
                self.new_prescription(event_data['prescription'])
                self._send_med_reminder(self._current_slot)
            elif event.data['type'] == 'update':
                self.update_prescription(event_data['prescription'])
                self._send_med_reminder(self._current_slot)
            elif event.data['type'] == 'delete':
                self.delete_prescription(event_data['prescription_id'])
        elif event.etype == 'slot_begin':
            self._current_slot = constants.get_slot_num(event.data['timetuple'])
            self._send_med_reminder(self._current_slot)
            self._set_next_slot_alarm(self._current_slot)
        else:
            print('unknown event in prescription manager', event)
            assert(False)

    
    def notify_user(self, what):
        self._evq.new_event(Event('alert', what))


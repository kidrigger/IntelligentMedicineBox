from event_queue import *

class PrescriptionManager:
    _prescriptions = []
    # assumed format of data in prescription {id : [{medicine : [slots] } ] }
    _slots = {}
    # slots is list of size 8
    _current_slot = 1
    _evq = None

    def __init__(self, evq):
        self._prescriptions = []
        self._slots = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8'}
        self._next_slot = 1
        self._evq = evq

    def new_prescription(self, prescription):
        self._prescriptions.append(prescription)

    def delete_prescription(self, prescription):
        self._prescriptions.remove(prescription)

    def update_prescription(self, prescription):
        for old_prescription in self._prescriptions:
            if old_prescription['id'] == prescription['id']:
                self.delete_prescription(old_prescription)
                break
        self.new_prescription(prescription)

    def notify_user(self):
        e1 = Event('timer', {'time' : str(self._slots[self._current_slot]), 'etype' : 'alert'})
        e2 = Event('timer', {'time' : str(self._slots[self._current_slot]), 'etype' : 'pres_man'})
        self._evq.new_event(e1)
        self._evq.new_event(e2)
        self._current_slot = self._current_slot + 1
        if self._current_slot == 9:
           self. _current_slot = 1

    def get_prescribed_medicine(self, slot):
        medicines = []
        for prescription in self._prescriptions:
            for medicine in prescription['id']:
                if medicine[slot] > 0:
                    medicines.append(medicine)
        return medicines

    def get_next_slot(self,slot):
        slot = slot + 1
        if slot == 9:
            slot = 1
        return [slot, self._slots[slot] ]

    def notify(self):
        self.notify_user()
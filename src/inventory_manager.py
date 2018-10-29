#!/bin/python3

"""
Inventory Manager
Stores and manages the inventory of the medicines.
"""
from event_queue import Event
import constants
from timer import get_current_time

class Inventory:
    _slot = []

    def __init__(self, slots= 6):
        self._slot = [0]*slots

class InventoryManager:
    _inventory = None
    _event_queue = None
    _medicines = None
    _medicine_at = None
    _slots = 0
    _delta = None
    
    def __init__(self, event_queue, slots=6):
        self._slots = slots
        self._inventory = Inventory(self._slots)
        self._event_queue = event_queue
        self._medicines = {}
        self._medicine_at = ['']*self._slots
        event_queue.register(self, ['weight_change'])

    def get_slot(self, med_name_or_index):
        if type(med_name_or_index) == int :
            med_index = med_name_or_index
            return self._inventory._slot[med_index]
        else:
            med_name = med_name_or_index
            return self._inventory._slot[ self._medicines[med_name]['loc'] ]

    def _put_at(self, index, medicine_name, med_info):
        self._medicines[medicine_name] = med_info
        self._medicine_at[index] = medicine_name
        self._medicines[medicine_name]['loc'] = index
        self._inventory._slot[index] = med_info['pills']

    def update_medicines(self, new_medicines):
        # If it's not possible to store these many medicines.
        if len(new_medicines) > self._slots:
            return None

        marked_for_removal = []
        list_meds = list(new_medicines.keys())

        # Mark all the old medicines for removal, if they are not needed again.	
        for i in range(0, self._slots):		
            if self._inventory._slot[i] != 0 and self._medicine_at[i] not in list_meds:
                marked_for_removal.append(i)

        new_med_index = 0
        new_med_count = len(new_medicines)
        
        # Fill all empty slots with new medicines first.
        for i in range(0, self._slots):	
            if new_med_index == new_med_count :
                return None
            if self._inventory._slot[i] == 0:
                medicine_name = list_meds[new_med_index]
                self._put_at(i, medicine_name, new_medicines[medicine_name])
                new_med_index += 1

        # If needed, overwrite old medicines.
        for i in marked_for_removal:	
            if new_med_index == new_med_count :
                return None
            medicine_name = list_meds[new_med_index]
            self._put_at(i, medicine_name, new_medicines[medicine_name])
            new_med_index += 1

    def get_inventory_data(self):
        med_count = {}
        for med in self._medicines:
            med_count[med] = self._inventory._slot[ self._medicines[med]['loc'] ]
        return med_count

    def notify(self, event):
        if event.etype == 'weight_change':
            slot_num = event.data['slot']
            med_name = self._medicine_at[slot_num]
            med_weight = self._medicines[med_name]['weight']
            diff = round(event.data['weight'] / med_weight) - self._inventory._slot[slot_num]
            self._inventory._slot[slot_num] = round(event.data['weight'] / med_weight)
            self._event_queue.new_event(Event('pill_change', {med_name: diff, 'medicine':med_name, 'time':event.data['time']} ))
            if self._delta == None or constants.is_stale(self._delta[0], event.data['time']):
                #print('hmm')
                self._delta = (event.data['time'], {med_name: diff})
                #print(constants.is_stale(self._delta[0]))
            elif med_name not in self._delta[1]:
                #print('hi')
                self._delta[1][med_name]= diff
            else: 
                #print('hello')
                self._delta[1][med_name]+= diff
            
    def get_inventory_delta(self, timetuple):
        if self._delta[0] >= timetuple[0] and self._delta[0] <= timetuple[1]:
            return self._delta[1]
        return None
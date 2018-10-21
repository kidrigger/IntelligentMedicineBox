from inventory_manager import *
from event_queue import *

class listener:
    record = []
    name = "listener"

    def __init__(self, name, evq, types = []):
        self.record = []
        evq.register(self, types)
        self.name = name
    
    def notify(self, ev):
        # print(self.name,'notified',ev.etype,ev.data)
        self.record.append(ev)
    
    def print_state(self):
        print(self.name,':')
        for ev in self.record:
            print('\t',ev.etype, ev.data)

    def clear(self):
        self.record = []

def test_inventory_manager_constructor():
	eq = EventQueue()
	inventory_man = InventoryManager(eq, 8)
	assert(inventory_man._slots == 8)
	assert(inventory_man._event_queue == eq)
	assert(len(inventory_man._medicine_at) == 8)

def test_update_medicines():
	eq = EventQueue()
	inventory_man = InventoryManager(eq, 8)
	medicines = {'abc': {'pills': 5}, 'alpha': {'pills': 4} }
	inventory_man.update_medicines(medicines)
	assert(inventory_man.get_slot('abc') == 5)
	assert(inventory_man.get_slot('alpha') == 4)
	assert(inventory_man.get_slot(0) == 5)
	assert(inventory_man.get_slot(1) == 4)

	medicines = {'aaa': {'pills': 19}, 'bbb': {'pills': 45}, 
	'ccc': {'pills': 10}, 'ddd': {'pills': 40}, 'eee': {'pills': 29}, 
	'fff': {'pills': 2} }
	inventory_man.update_medicines(medicines)
	assert(inventory_man.get_slot('abc') == 5)
	assert(inventory_man.get_slot('alpha') == 4)
	assert(inventory_man.get_slot('aaa') == 19)
	assert(inventory_man.get_slot('bbb') == 45)
	assert(inventory_man.get_slot('ccc') == 10)
	assert(inventory_man.get_slot('ddd') == 40)
	assert(inventory_man.get_slot('eee') == 29)
	assert(inventory_man.get_slot('fff') == 2)
		
	assert(inventory_man.get_slot(0) == 5)
	assert(inventory_man.get_slot(1) == 4)
	assert(inventory_man.get_slot(2) == 19)
	assert(inventory_man.get_slot(3) == 45)
	assert(inventory_man.get_slot(4) == 10)
	assert(inventory_man.get_slot(5) == 40)
	assert(inventory_man.get_slot(6) == 29)
	assert(inventory_man.get_slot(7) == 2)

def test_overwriting_med():
	eq = EventQueue()
	inventory_man = InventoryManager(eq, 8)
	medicines = {'aaa': {'pills': 19}, 'bbb': {'pills': 45}, 
	'ccc': {'pills': 10}, 'ddd': {'pills': 40}, 'eee': {'pills': 29}, 
	'fff': {'pills': 2}, 'ggg': {'pills':3}, 'hhh': {'pills':5} }
	inventory_man.update_medicines(medicines)
	medicines = {'abc': {'pills': 1}, 'alpha': {'pills': 2} }
	inventory_man.update_medicines(medicines)
	assert(inventory_man.get_slot('abc') == 1)
	assert(inventory_man.get_slot('alpha') == 2)
	assert(inventory_man.get_slot(0) == 1)
	assert(inventory_man.get_slot(1) == 2)

	assert(inventory_man.get_slot('ccc') == 10)
	assert(inventory_man.get_slot('ddd') == 40)
	assert(inventory_man.get_slot('eee') == 29)
	assert(inventory_man.get_slot('fff') == 2)
	assert(inventory_man.get_slot('ggg') == 3)
	assert(inventory_man.get_slot('hhh') == 5)
	
	assert(inventory_man.get_slot(2) == 10)
	assert(inventory_man.get_slot(3) == 40)
	assert(inventory_man.get_slot(4) == 29)
	assert(inventory_man.get_slot(5) == 2)
	assert(inventory_man.get_slot(6) == 3)
	assert(inventory_man.get_slot(7) == 5)

def test_get_inventory_data():
	eq = EventQueue()
	inventory_man = InventoryManager(eq, 8)
	medicines = {'aaa': {'pills': 19}, 'bbb': {'pills': 45}, 
	'ccc': {'pills': 10}, 'ddd': {'pills': 40}, 'eee': {'pills': 29}, 
	'fff': {'pills': 2}, 'ggg': {'pills':3}, 'hhh': {'pills':5} }
	inventory_man.update_medicines(medicines)
	inventory = inventory_man.get_inventory_data()
	assert(len(inventory)==8)
	assert(inventory['aaa'] == 19)
	assert(inventory['bbb'] == 45)
	assert(inventory['ccc'] == 10)
	assert(inventory['ddd'] == 40)
	assert(inventory['eee'] == 29)
	assert(inventory['fff'] == 2)
	assert(inventory['ggg'] == 3)
	assert(inventory['hhh'] == 5)

def test_notify():
	eq = EventQueue(['weight_change', 'pill_change'])
	inventory_man = InventoryManager(eq, 2)
	medicines = {'abc': {'pills': 5, 'weight': 0.1}, 'alpha': {'pills': 2, 'weight': 0.2} }
	inventory_man.update_medicines(medicines)
	eq.register(inventory_man, ['weight_change'])
	listener_ = listener('pill listener', eq, ['pill_change'])
	event = Event('weight_change', {'slot': 0, 'weight': 0.3})
	eq.new_event(event)
	eq.update()
	eq.update()
	assert(len(listener_.record)==1)
	assert(listener_.record[0].etype=='pill_change')
	assert(listener_.record[0].data['abc'] == -2)
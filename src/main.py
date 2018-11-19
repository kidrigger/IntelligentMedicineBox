from event_queue import *
from prescription_manager import PrescriptionManager
from inventory_manager import InventoryManager
from timer import *
from notifier import Notifier
from time import sleep
from anomaly import Anomaly
import getpass

def main():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert', 'new_pres', 'timer','slot_begin'])
	prescription_manager = PrescriptionManager(event_queue)	
	inventory_manager = InventoryManager(event_queue)
	timer = Timer(event_queue)

	anomaly = Anomaly(inventory_manager, prescription_manager, event_queue)
	email = input('Please enter patient email id: ')
	password = getpass.getpass('Please enter patient password: ')
	notifier = Notifier(event_queue, email, password)
	print ('All objects created')
	
	prescription = {'id': '1', 'medicines':{'abc':[2, 1, 1, 1, 1, 1, 1, 1], 'def':[2, 2, 1, 2, 1, 1, 2, 1]}, 'expiry_date':'12/11/2018' }
	new_prescription = Event('presc_man', {'type': 'new', 'prescription':prescription})
	event_queue.new_event(new_prescription)
	
	medicines = {'abc': {'pills': 50, 'weight':0.1}, 'def': {'pills': 40, 'weight':0.2} }
	inventory_manager.update_medicines(medicines)
	print ('Initialised all objects')
	print(event_queue._event_queue)
	event_queue.update()
	sleep(1)

	while(True):
		slot_num= input('>>>')
		if slot_num != '-1':
			slot_num = int(slot_num)
			weight = float(input())
			event = Event('weight_change', {'slot': slot_num, 'weight': weight, 'time': get_current_time()})
			event_queue.new_event(event)
		print(event_queue._event_queue)
		#print("In main")
		event_queue.update()
		sleep(60)

main()

from anomaly import *
from event_queue import *
from inventory_manager import *
from prescription_manager import *

class listener:
    record = []
    name = "listener"

    def __init__(self, evq, types = []):
        self.record = []
        evq.register(self, types)
    
    def notify(self, ev):
        # print(self.name,'notified',ev.etype,ev.data)
        self.record.append(ev)
    
def test_notify():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	listener_ = listener(event_queue, ['alert'])
	medicines = {'abc': {'pills': 5, 'weight':0.1}, 'alpha': {'pills': 4, 'weight':0.2} }
	inventory_manager.update_medicines(medicines)
	event = Event('weight_change', {'slot': 1, 'weight': 0.3, 'time':'09:00'})
	event_queue.new_event(event)
	event_queue.update() # inventory manager receives a weight_change event.
	event_queue.update() # inventory manager sends out a pill_change event, which anomaly detector listens to.
	# Now anomaly finds out that this is not in the current slot of prescription.
	# Hence, emits a wrong med notification.
	event_queue.update()
	assert(len(listener_.record)==1)
	event = listener_.record[0]
	assert(event.etype=='alert')
	assert(event.data['type']=='wrongmed')	

def test_check_wrong_dose():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	listener_ = listener(event_queue, ['alert'])
	medicines = {'abc': {'pills': 5, 'weight':0.1}, 'alpha': {'pills': 4, 'weight':0.2} }
	inventory_manager.update_medicines(medicines)
	event = Event('weight_change', {'slot': 1, 'weight': 0.3, 'time':'09:00'})
	event_queue.new_event(event)
	event_queue.update() # inventory manager receives a weight_change event.
	event_queue.update() # inventory manager sends out a pill_change event, which anomaly detector listens to.
	# Now anomaly finds out that this is not in the current slot of prescription.
	# Hence, emits a wrong med notification.
	event_queue.update()
	assert(len(listener_.record)==1)
	event = listener_.record[0]
	assert(event.etype=='alert')
	assert(event.data['type']=='wrongmed')	

def test_check_overdose():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'def':[0, 0, 1, 2, 1, 0, 0, 1]} }
	prescription_manager.new_prescription(prescription)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	listener_ = listener(event_queue, ['alert'])

	medicines = {'abc': {'pills': 5, 'weight':0.1}, 'alpha': {'pills': 4, 'weight':0.2} }
	inventory_manager.update_medicines(medicines)
	event = Event('weight_change', {'slot': 0, 'weight': 0.3, 'time':'09:00'})
	event_queue.new_event(event)
	event_queue.update() # inventory manager receives a weight_change event.
	event_queue.update() # inventory manager sends out a pill_change event, which anomaly detector listens to.
	# Now anomaly finds out that this is more than prescription.
	# Hence, emits an overdose notification.
	event_queue.update()
	assert(len(listener_.record)==1)
	event = listener_.record[0]
	assert(event.etype=='alert')
	assert(event.data['type']=='overdose')	

def test_check_underdose():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'alpha':[0, 0, 1, 2, 1, 0, 0, 1]} }
	prescription_manager.new_prescription(prescription)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	listener_ = listener(event_queue, ['alert'])

	medicines = {'abc': {'pills': 50, 'weight':0.1}, 'alpha': {'pills': 40, 'weight':0.1} }
	inventory_manager.update_medicines(medicines)
	event = Event('weight_change', {'slot': 1, 'weight': 3.9, 'time':'13:39'})
	#patient picks first pill.
	event_queue.new_event(event)
	event_queue.update() # inventory manager receives a weight_change event.
	event_queue.update() # inventory manager sends out a pill_change event, which anomaly detector listens to.
	# Now anomaly finds out that this is less than prescription.
	# Hence, emits an underdose notification.
	event_queue.update()
	assert(len(listener_.record)==1)
	event = listener_.record[0]
	assert(event.etype=='alert')
	assert(event.data['type']=='underdose')	
	listener_.record.clear()

	event = Event('weight_change', {'slot': 1, 'weight': 3.8, 'time':'13:40'})
	# Patient picks up the second pill.
	event_queue.new_event(event)
	event_queue.update() # inventory manager receives a weight_change event.
	event_queue.update() # inventory manager sends out a pill_change event, which anomaly detector listens to.
	# Now anomaly finds out that this is less than prescription.
	# Hence, emits an underdose notification.
	event_queue.update()
	assert(len(listener_.record)==0)

#def test_slot_end_anomaly():

def test_set_reminder():	
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert', 'timer'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'alpha':[0, 0, 1, 2, 1, 0, 0, 1]} }
	prescription_manager.new_prescription(prescription)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	anomaly_detector._set_reminder(constants.get_slot_time(0))
	assert(len(event_queue._event_queue['timer'])==1)
	event = event_queue._event_queue['timer'][0]
	assert(event.data['time']==constants.get_slot_time(1)[1])
	assert(event.data['etype']=='slot_end')
	assert(event.data['timetuple']==constants.get_slot_time(1))

def test_anomaly_notifier():
	event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change', 'presc_man', 'timeslot', 'alert', 'timer'])
	inventory_manager = InventoryManager(event_queue, 6)
	prescription_manager = PrescriptionManager(event_queue)
	prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'alpha':[0, 0, 1, 2, 1, 0, 0, 1]} }
	prescription_manager.new_prescription(prescription)
	anomaly_detector = Anomaly(inventory_manager, prescription_manager, event_queue)
	anomaly_detector._anomaly_notifier({'msg':'foo', 'type':'wrongmed'})
	assert(len(event_queue._event_queue['alert'])==1)
	event = event_queue._event_queue['alert'][0]
	assert(event.data['type']=='wrongmed')
	assert(event.data['msg']=='foo')
	

#if __name__=='__main__':
#	test_notify()
#	test_check_wrong_dose()
#	test_check_overdose()
#	test_check_underdose()
#	test_set_reminder()
#	test_anomaly_notifier()
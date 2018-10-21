from unittest.mock import *
from anomaly import *

class Testclass:
	def __init__(self):
		pass

def test_notify():
	event = Event('anmly',[0,0])
	inventory_manager.get_inventory_delta = Mock(return_value={})
	prescription_manager.get_prescribed_med = Mock(return_value={})
	anmly.notify(event)
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(0)

def test_anomaly_detector():
	inventory_manager.get_inventory_delta = Mock(return_value={'A':2})
	prescription_manager.get_prescribed_med = Mock(return_value={})
	anmly._anomaly_detector([1,0])
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(1)
	event_queue.new_event.assert_called()

	inventory_manager.get_inventory_delta = Mock(return_value={'A':2})
	prescription_manager.get_prescribed_med = Mock(return_value={'A':1})
	anmly._anomaly_detector([0,0])
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(0)
	event_queue.new_event.assert_called()

	inventory_manager.get_inventory_delta = Mock(return_value={'A':1})
	prescription_manager.get_prescribed_med = Mock(return_value={'A':2})
	anmly._anomaly_detector([2,0])
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(2)
	event_queue.new_event.assert_called()
	
	inventory_manager.get_inventory_delta = Mock(return_value={})
	prescription_manager.get_prescribed_med = Mock(return_value={'B':2})
	anmly._anomaly_detector([0,0])
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(0)
	event_queue.new_event.assert_called()

	inventory_manager.get_inventory_delta = Mock(return_value={'A':1})
	prescription_manager.get_prescribed_med = Mock(return_value={'A':1})
	anmly._anomaly_detector([4,0])
	inventory_manager.get_inventory_delta.assert_called_once()
	prescription_manager.get_prescribed_med.assert_called_once_with(4)
	event_queue.new_event.assert_called()

def test_create_data():
	assert anmly._create_data('A','B') == {'msg':'A', 'type':'B'}


def test_set_reminder():
	anmly._set_reminder([0,0])
	prescription_manager.get_next_slot.assert_called_with(0)
	event_queue.new_event.assert_called()

def test_anomaly_notifier():
	
	anmly._anomaly_notifier({'msg':'foo','type':'wrongmed'})
	event_queue.new_event.assert_called()

if __name__=='__main__':
	inventory_manager = Testclass()
	prescription_manager = Testclass()
	event_queue = Testclass()
	event_queue.new_event = Mock(return_value=1)
	prescription_manager.get_next_slot = Mock(return_value=[1,30])
	anmly = Anomaly(inventory_manager,prescription_manager,event_queue)
	test_notify()
	test_anomaly_detector()
	test_create_data()
	test_set_reminder()
	test_anomaly_notifier()


import unittest
from unittest.mock import *
from anomaly import *

class Testclass:
	def __init__(self):
		pass
class MyTest(unittest.TestCase):

	# def __init__(self):
	inventory_manager = Testclass()
	prescription_manager = Testclass()
	event_queue = Testclass()
	event_queue.new_event = Mock(return_value=1)
	event_queue.register = Mock(return_value=1)
	prescription_manager.get_next_slot = Mock(return_value=(1,('0','30')))
	anmly = Anomaly(inventory_manager,prescription_manager,event_queue)

	def test_notify(self):
		event = Event('anmly',{'time':(1,('0','30'))})
		self.inventory_manager.get_inventory_delta = Mock(return_value={})
		self.prescription_manager.get_prescribed_med = Mock(return_value={})
		self.anmly.notify(event)
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(1)

	def test_anomaly_detector(self):
		self.inventory_manager.get_inventory_delta = Mock(return_value={'A':2})
		self.prescription_manager.get_prescribed_med = Mock(return_value={})
		self.anmly._anomaly_detector((1,('21','22')))
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(1)
		self.event_queue.new_event.assert_called()

		self.inventory_manager.get_inventory_delta = Mock(return_value={'A':2})
		self.prescription_manager.get_prescribed_med = Mock(return_value={'A':1})
		self.anmly._anomaly_detector((0,('1','2')))
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(0)
		self.event_queue.new_event.assert_called()

		self.inventory_manager.get_inventory_delta = Mock(return_value={'A':1})
		self.prescription_manager.get_prescribed_med = Mock(return_value={'A':2})
		self.anmly._anomaly_detector((2,('11','12')))
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(2)
		self.event_queue.new_event.assert_called()
		
		self.inventory_manager.get_inventory_delta = Mock(return_value={})
		self.prescription_manager.get_prescribed_med = Mock(return_value={'B':2})
		self.anmly._anomaly_detector((0,('10','12')))
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(0)
		self.event_queue.new_event.assert_called()

		self.inventory_manager.get_inventory_delta = Mock(return_value={'A':1})
		self.prescription_manager.get_prescribed_med = Mock(return_value={'A':1})
		self.anmly._anomaly_detector((4,('0','2')))
		self.inventory_manager.get_inventory_delta.assert_called_once()
		self.prescription_manager.get_prescribed_med.assert_called_once_with(4)
		self.event_queue.new_event.assert_called()

	def test_create_data(self):
		self.assertEqual(self.anmly._create_data('A','B'),{'msg':'A', 'type':'B'})


	def test_set_reminder(self):
		self.anmly._set_reminder((2,('0','1')))
		self.prescription_manager.get_next_slot.assert_called_with(2)
		self.event_queue.new_event.assert_called()

	def test_anomaly_notifier(self):
		self.anmly._anomaly_notifier({'msg':'foo','type':'wrongmed'})
		self.event_queue.new_event.assert_called()

if __name__=='__main__':
	unittest.main()
	

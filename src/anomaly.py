"""
Anomaly Detector
checks if medicine taken properly and if not, sends notification

version: 2.0
"""
from event_queue import *

class Anomaly:

	_inventory_manager = None
	_prescription_manager = None
	_event_queue = None

	def _set_reminder(self,time):
		#set reminder at 
		time = self._prescription_manager.get_next_slot(time[0])
		end_time = time[1] + 130
		if (end_time%100)>=60:
			end_time+=40
		event = Event('timer',{'time':str(end_time),'etype':'anmly','data':time})
		self._event_queue.new_event(event)

	def __init__(self, inventory_manager, prescription_manager, event_queue):
		self._inventory_manager = inventory_manager
		self._prescription_manager = prescription_manager
		self._event_queue = event_queue
		self._set_reminder([8,0])

				
	def _create_data(self,message,atype):
		return {'msg':message, 'type':atype}


	def _anomaly_detector(self,time):
		meds_consumed = self._inventory_manager.get_inventory_delta()
		meds_prescribed = self._prescription_manager.get_prescribed_med(time[0])

		for med in meds_consumed:

			if med not in meds_prescribed:
				message = "You are not supposed to consume "+str(med)+" at this time"
				self._anomaly_notifier(self._create_data(message,'wrongmed'))

			else:
				if meds_consumed[med]>meds_prescribed[med]:
					message = "You have consumed "+str(meds_consumed[med]-meds_prescribed[med])+" extra pills of "+str(med)
					self._anomaly_notifier(self._create_data(message,'overdose'))

				elif meds_consumed[med]<meds_prescribed[med]:
					message = "You have to consume "+str(meds_prescribed[med]-meds_consumed[med])+" more pills of "+str(med)
					self._anomaly_notifier(self._create_data(message,'underdose'))

		for med in meds_prescribed:

			if med not in meds_consumed:
				message = "You have to consume "+str(meds_prescribed[med])+" pills of "+str(med)
				self._anomaly_notifier(self._create_data(message,'underdose'))

		self._set_reminder(time)


	def notify(self,event):
		time = event.data
		self._anomaly_detector(time)


	def _anomaly_notifier(self, data):
		#create notification event
		anmly = Event('alert',data)
		self._event_queue.new_event(anmly)


	# def _get_meds_taken(self):
	# 	meds_consumed = {}
	# 	current_inventory = _inventory_manager.get_inventory()
	# 	for med in current_inventory:
	# 		if med in _inventory:
	# 			quantitiy_consumed = _inventory[med]-current_inventory[med]
	# 			if quantitiy_consumed>0:
	# 				meds_consumed[med]=quantitiy_consumed
	# 	_inventory = current_inventory
	# 	return meds_consumed
	# new medicine added in slot can only be checked for anmly from next slot
"""
Anomaly Detector
checks if medicine taken properly and if not, sends notification

version: 2.0
"""
from event_queue import *
import constants

class Anomaly:

	_inventory_manager = None
	_prescription_manager = None
	_event_queue = None

	def _set_reminder(self, time):
		#set reminder at end of timeslot 
		next_slot_index = self._prescription_manager.get_next_slot(constants.get_slot_num(time))
		time = constants.get_slot_time(next_slot_index)
		event = Event('timer', {'time':time[1], 'etype':'slot_end', 'timetuple':time} )
		self._event_queue.new_event(event)

	def __init__(self, inventory_manager, prescription_manager, event_queue):
		self._inventory_manager = inventory_manager
		self._prescription_manager = prescription_manager
		self._event_queue = event_queue
		self._event_queue.register(self, ['slot_end', 'pill_change'])
		#self._set_reminder(8, ('00:00', '00:00') )
				
	def _create_data(self,message,atype):
		return {'msg':message, 'type':atype}


	def _check_wrong_dose(self, med_name, meds_prescribed):
		if med_name not in meds_prescribed:
			message = "You are not supposed to consume "+ med_name +" at this time"
			self._anomaly_notifier(self._create_data(message, 'wrongmed'))
			return True
		return False

	def _check_overdose(self, med_name, pills, meds_prescribed):
		if pills > meds_prescribed[med_name]:
			message = "You have consumed "+str(pills - meds_prescribed[med_name])+" extra pills of " + med_name 
			self._anomaly_notifier(self._create_data(message,'overdose'))

	def _check_underdose(self, med_name, pills, meds_prescribed):
		if pills < meds_prescribed[med_name]:
			message = "You have to consume "+str(meds_prescribed[med_name] - pills)+" more pills of " + med_name
			self._anomaly_notifier(self._create_data(message,'underdose'))


	def _anomaly_detector(self, timetuple, med_name=None):
		meds_consumed = self._inventory_manager.get_inventory_delta(timetuple)
		curr_time_slot = constants.get_slot_num(timetuple)
		meds_prescribed = self._prescription_manager.get_prescribed_medicine(curr_time_slot)

		if med_name == None:
			for med in meds_consumed:
				if not self._check_wrong_dose(med, meds_prescribed):
					pills = meds_consumed[med]
					self._check_overdose(med, -pills, meds_prescribed)
					self._check_underdose(med, -pills, meds_prescribed)
			for med in meds_prescribed:
				if med not in meds_consumed:
					message = "You have to consume "+str(meds_prescribed[med])+" pills of "+ med
					self._anomaly_notifier(self._create_data(message, 'underdose' ))

		else:
			if not self._check_wrong_dose(med_name, meds_prescribed):
				print(meds_consumed)
				pills_taken = meds_consumed[med_name]
				self._check_overdose(med_name, -pills_taken, meds_prescribed)
				self._check_underdose(med_name, -pills_taken, meds_prescribed)
		#self._set_reminder(timetuple)
		
		        
	def notify(self,event):
		if event.etype == 'slot_end':
			timetuple = event.data['timetuple'] #Based on the timer event its passing into event_queue.
			self._anomaly_detector(timetuple)
			self._set_reminder(timetuple)

		elif event.etype == 'pill_change':
			med_name = event.data['medicine']
			print(event.etype, event.data)
			self._anomaly_detector(event.data['time'], med_name)


	def _anomaly_notifier(self, data):
		#create notification event
		anmly = Event('alert',data)
		self._event_queue.new_event(anmly)

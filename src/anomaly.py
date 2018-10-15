"""
Anomaly Detector
checks if medicine taken is correct and if not, sends notification

version: 1.0
"""
class Anomaly:
	def anomaly_detector(self,InventoryManager,PrescriptionManager,EventQueue):
		meds_consumed = InventoryManager.get_meds_taken()
		meds_prescribed = PrescriptionManager.get_prescribed_med()
		for med in meds_consumed:
			if med not in meds_prescribed:
				_wrongmed_anomaly(EventQueue,med)
			else:
				if meds_consumed[med]>meds_prescribed[med]:
					_overdose_anomaly(EventQueue,{med:meds_consumed[med]-meds_prescribed[med]})
				elif meds_consumed[med]<meds_prescribed[med]:
					_underdose_anomaly(EventQueue,{med:meds_prescribed[med]-meds_consumed[med]})

	def _overdose_anomaly(self,EventQueue,data):
		#create event
		overdose = Event()
		overdose.etype = 'ovrdamly'
		overdose.data = data
		EventQueue.new_event(overdose)

	def _underdose_anomaly(self,EventQueue,data):
		#create event
		underdose = Event()
		underdose.etype = 'undrdamly'
		underdose.data = data
		EventQueue.new_event(underdose)

	def _wrongmed_anomaly(self,EventQueue,data):
		#create event
		wrongmed = Event()
		wrongmed.etype = 'wrngamly'
		wrongmed.data = data
		EventQueue.new_event(wrongmed)

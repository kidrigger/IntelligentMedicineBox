class PrescriptionManager:
    _prescriptions = []

    def new_prescription(self, prescription):
        self._prescriptions.append(prescription)

    def delete_prescription(self, prescription):
        self._prescriptions.remove(prescription)

    def update_prescription(self, old_prescription, new_prescription):
        if old_prescription in self._prescriptions:
            self._prescriptions.remove(old_prescription)
        self._prescriptions.append(new_prescription)

    def notify_user(self):
        event = Event('alert','from_prescription_manager')
        Notifier.notify(event)

    def get_prescribed_medicine(self,time):
        for prescription in self._prescriptions:
            if prescription.time == time:
                return prescription.medicies
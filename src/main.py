from event_queue import *
from prescription_manager import PrescriptionManager
from inventory_manager import InventoryManager
from timer import *
from notifier import Notifier
from time import sleep
from anomaly import Anomaly
import getpass
from threading import Lock, Thread
import tkinter


class Main:

    def main(self):
        self.event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change',
                                       'presc_man', 'timeslot', 'alert', 'new_pres', 'timer', 'slot_begin'])
        prescription_manager = PrescriptionManager(self.event_queue)
        inventory_manager = InventoryManager(self.event_queue)
        self.timer = Timer(self.event_queue)

        anomaly = Anomaly(inventory_manager,
                          prescription_manager, self.event_queue)
        email = input('Please enter patient email id: ')
        password = getpass.getpass('Please enter patient password: ')
        notifier = Notifier(self.event_queue, email, password)
        print ('All objects created')

        prescription = {'id': '1', 'medicines': {'abc': [2, 1, 1, 1, 1, 1, 1, 1], 'def': [
            2, 2, 1, 2, 1, 1, 2, 1]}, 'expiry_date': '12/11/2018'}
        new_prescription = Event(
            'presc_man', {'type': 'new', 'prescription': prescription})
        self.event_queue.new_event(new_prescription)

        medicines = {'abc': {'pills': 50, 'weight': 0.1},
                     'def': {'pills': 40, 'weight': 0.2}}
        inventory_manager.update_medicines(medicines)
        print ('Initialised all objects')
        print(self.event_queue._event_queue)
        self.event_queue.update()
        sleep(1)

        self.lock = threading.Lock()
        self.running = True
        self.thr = threading.Thread(target=self.mainloop)
        self.thr.start()

        self.main_wid = tkinter.Tk()

        self.label_wid = tkinter.LabelFrame(
            self.main_wid, text="Enter Slot Number")
        self.label_wid.pack()

        self.slot_entry_wid = tkinter.Entry(self.label_wid)

        self.slot_entry_wid.pack()
        self.slot_entry_wid.focus_set()

        self.new_weight_entry_label = tkinter.LabelFrame(
            self.main_wid, text="Enter New Slot Weight")
        self.new_weight_entry_label.pack()

        self.weight_entry = tkinter.Entry(self.new_weight_entry_label)
        self.weight_entry.pack()
        self.new_weight_entry_label.focus_set()

        self.submit_button = tkinter.Button(
            self.main_wid, text="Submit", command=self.submit_cmd)
        self.submit_button.pack()

        self.main_wid.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_wid.mainloop()

        # print("END")

    def mainloop(self):
        while self.running:
            self.lock.acquire()
            print(self.event_queue._event_queue)
            print("In main")
            self.event_queue.update()
            self.lock.release()
            sleep(10)
        #print("MAINLOOP END")

    def submit_cmd(self):
        weight = -1
        slot = -1
        slot_txt = self.slot_entry_wid.get()
        if (slot_txt != ""):
            slot = int(slot_txt)
        weight_txt = self.weight_entry.get()
        if (weight_txt != ""):
            weight = float(weight_txt)
        print(slot, weight)
        event = Event('weight_change', {
                      'slot': slot, 'weight': weight, 'time': get_current_time()})
        self.lock.acquire()
        self.event_queue.new_event(event)
        self.lock.release()

    def on_closing(self):
        self.running = False
        self.main_wid.destroy()
        self.thr.join()
        self.timer.stop()
        # print("EXIT WINDOW")


ma = Main()
ma.main()

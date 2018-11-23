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

        self.logged_in = False

        self.event_queue = EventQueue(['slot_end', 'weight_change', 'pill_change',
                                       'presc_man', 'timeslot', 'alert', 'new_pres', 'timer', 'slot_begin'])
        self.prescription_manager = PrescriptionManager(self.event_queue)
        self.inventory_manager = InventoryManager(self.event_queue)
        self.timer = Timer(self.event_queue)

        self.anomaly = Anomaly(self.inventory_manager,
                               self.prescription_manager, self.event_queue)

        width = 300
        height = 200
        self.main_wid = tkinter.Tk()

        # Center the window
        self.main_wid.update_idletasks()
        x = (self.main_wid.winfo_screenwidth() // 2) - (width // 2)
        y = (self.main_wid.winfo_screenheight() // 2) - (height // 2)
        self.main_wid.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Add title
        self.main_wid.title("IntelligentMedicineBox")
        self.email_wid_label = tkinter.LabelFrame(
            self.main_wid, text="Enter login")
        self.email_wid = tkinter.Entry(self.email_wid_label)
        self.pass_wid_label = tkinter.LabelFrame(
            self.main_wid, text="Enter password")
        self.pass_wid = tkinter.Entry(self.pass_wid_label, show='*')
        self.email_wid_label.pack(anchor='center')
        self.email_wid.pack(anchor='center')
        self.pass_wid_label.pack(anchor='center')
        self.pass_wid.pack(anchor='center')
        self.login_button = tkinter.Button(
            self.main_wid, text="Login", command=self.login_cmd)
        self.login_button.pack(anchor='center')

        self.notifier = Notifier(self.event_queue)

        self.lock = threading.Lock()
        self.running = True
        self.thr = threading.Thread(target=self.mainloop)
        self.thr.start()

        self.label_wid = tkinter.LabelFrame(
            self.main_wid, text="Enter Slot Number")

        self.slot_entry_wid = tkinter.Entry(self.label_wid)

        self.slot_entry_wid.focus_set()

        self.new_weight_entry_label = tkinter.LabelFrame(
            self.main_wid, text="Enter New Slot Weight")

        self.weight_entry = tkinter.Entry(self.new_weight_entry_label)
        self.new_weight_entry_label.focus_set()

        self.submit_button = tkinter.Button(
            self.main_wid, text="Submit", command=self.submit_cmd)

        self.main_wid.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.main_wid.mainloop()

        # print("END")

    def mainloop(self):

        while not self.logged_in:
            if not self.running:
                return
            sleep(1)

        prescription = {'id': '1', 'medicines': {'abc': [2, 1, 1, 1, 1, 1, 1, 1], 'def': [
            2, 2, 1, 2, 1, 1, 2, 1]}, 'expiry_date': '12/11/2018'}
        new_prescription = Event(
            'presc_man', {'type': 'new', 'prescription': prescription})
        self.event_queue.new_event(new_prescription)
        medicines = {'abc': {'pills': 50, 'weight': 0.1},
                     'def': {'pills': 40, 'weight': 0.2}}
        self.inventory_manager.update_medicines(medicines)
        print ('Initialised all objects')
        print(self.event_queue._event_queue)
        self.event_queue.update()
        sleep(1)

        while self.running:
            self.lock.acquire()
            print(self.event_queue._event_queue)
            print("In main")
            self.event_queue.update()
            self.lock.release()
            sleep(10)
        # print("MAINLOOP END")

    def login_cmd(self):
        email = self.email_wid.get()
        password = self.pass_wid.get()
        valid_email = self.notifier.pyrebase_init(email, password)
        if not valid_email:
            tkinter.messagebox.showerror(
                "Auth Error", "ID or Password incorrect")
        else:
            self.email_wid_label.pack_forget()
            self.email_wid.pack_forget()
            self.pass_wid_label.pack_forget()
            self.pass_wid.pack_forget()
            self.login_button.pack_forget()
            self.label_wid.pack()
            self.slot_entry_wid.pack()
            self.new_weight_entry_label.pack()
            self.weight_entry.pack()
            self.submit_button.pack()
            self.logged_in = True

    def submit_cmd(self):
        weight = -1
        slot = -1
        try:
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
        except:
            print("Invalid input please check.")

    def on_closing(self):
        self.running = False
        self.main_wid.destroy()
        self.thr.join()
        self.timer.stop()
        # print("EXIT WINDOW")


ma = Main()
ma.main()

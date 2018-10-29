from timer import get_current_time

slots = [('06:30','08:00'),('08:00','09:30'),('11:30','13:00'),('13:00','14:30'),('15:30','17:00'),('17:00','18:30'),('19:30','21:00'),('21:00','22:30')]

def get_slot_time(slot_num):
    return slots[slot_num]

def get_slot_num(time):
    if type(time) == tuple:
        time = time[0]
    for i in range(0, 8):
        if slots[i][0] <= time and time <= slots[i][1]:
            return i

def is_stale(time, current_time=None):
    if current_time==None:
        return get_slot_num(time) != get_slot_num(get_current_time())
    else:
        return get_slot_num(time) != get_slot_num(current_time)    

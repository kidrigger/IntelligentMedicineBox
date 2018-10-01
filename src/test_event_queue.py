
from event_queue import *

class listener:
    record = []
    name = "listener"

    def __init__(self, name, evq, types = []):
        self.record = []
        evq.register(self, types)
        self.name = name
    
    def notify(self, ev):
        # print(self.name,'notified',ev.etype,ev.data)
        self.record.append(ev)
    
    def print_state(self):
        print(self.name,':')
        for ev in self.record:
            print('\t',ev.etype, ev.data)

    def clear(self):
        self.record = []

def test_evgen():

    evq = EventQueue(['t1','t2'])

    evq.new_event(Event('t1',{'f1':'foo'}))

    assert(len(evq._event_queue['t1']) == 1)
    assert(evq._event_queue['t1'][0].etype == 't1')
    assert(evq._event_queue['t1'][0].data['f1'] == 'foo')
    assert(len(evq._event_queue['t2']) == 0)

def test_evregister():

    evq = EventQueue(['t1','t2','t3'])

    lis1 = listener('lis1', evq, ['t1','t2'])
    lis2 = listener('lis2', evq, ['t3'])
    
    assert(len(evq._event_listeners['t1']) == 1)
    assert(len(evq._event_listeners['t2']) == 1)
    assert(len(evq._event_listeners['t3']) == 1)

    assert(evq._event_listeners['t1'][0] == lis1)
    assert(evq._event_listeners['t2'][0] == lis1)
    assert(evq._event_listeners['t3'][0] == lis2)


def test_evnotify():

    evq = EventQueue(['t1','t2','t3'])

    lis1 = listener('lis1', evq, ['t1','t2'])
    lis2 = listener('lis2', evq, ['t2','t3'])

    evq.new_event(Event('t1',{'f1':'foo'}))
    evq.update()

    assert(len(lis1.record) == 1)
    assert(lis1.record[0].etype == 't1')
    assert(lis1.record[0].data['f1'] == 'foo')
    assert(len(lis2.record) == 0)
    lis1.clear()
    lis2.clear()

    evq.new_event(Event('t3',{'f1':'foo'}))
    evq.update()

    assert(len(lis2.record) == 1)
    assert(lis2.record[0].etype == 't3')
    assert(lis2.record[0].data['f1'] == 'foo')
    assert(len(lis1.record) == 0)
    lis1.clear()
    lis2.clear()

    evq.new_event(Event('t2',{'f1':'foo'}))
    evq.update()

    assert(len(lis1.record) == 1)
    assert(lis1.record[0].etype == 't2')
    assert(lis1.record[0].data['f1'] == 'foo')
    assert(len(lis2.record) == 1)
    assert(lis2.record[0].etype == 't2')
    assert(lis2.record[0].data['f1'] == 'foo')
    lis1.clear()
    lis2.clear()
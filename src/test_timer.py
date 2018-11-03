from timer import *
from datetime import datetime, timedelta
from event_queue import *
import threading
import time

class listener:
    record = []
    name = "listener"

    def __init__(self, name, evq, types = []):
        self.record = []
        evq.register(self, types)
        self.name = name
    
    def notify(self, ev):
        #print(self.name, 'notified', ev.etype, ev.data)
       	self.record.append(ev)

def create_alarm(time):
	delta = timedelta(minutes=time)
	time = datetime.now() + delta
	time_str = '{:%H:%M}'.format(time)
	return time_str

def test_notify():
	event_queue = EventQueue(['timer'])
	timer = Timer(event_queue)
	event  = Event('timer', {'time': create_alarm(1), 'etype': 'test1'})
	assert(len(timer._alarm_time_queue)==0)
	timer.notify(event)
	assert(len(timer._alarm_time_queue)==1)
	timer.stop()
	
def test_timer():
	event_queue = EventQueue(['test1', 'timer', 'test2'])
	timer = Timer(event_queue)
	time_interval = 60 							# Update event queue after every 60 seconds.
	listener_ = listener('a listener', event_queue, ['test1', 'test2'])

	event  = Event('timer', {'time': create_alarm(1), 'etype': 'test1'})
	event2 = Event('timer', {'time': create_alarm(2), 'etype': 'test2'})
	event_queue.new_event(event)
	event_queue.new_event(event2)
	#timer_stop = threading.Event()
	
	event_queue.update()
	assert(len(listener_.record)==0)

	time.sleep(61)
	event_queue.update()
	assert(len(listener_.record)==1)

	time.sleep(60)
	event_queue.update()
	assert(len(listener_.record)==2)

	print("Basic timer test passed!")
	timer.stop()

def test_one_to_many():
	event_queue = EventQueue(['timer', 'test1', 'test2', 'test3', 'test4', 'test5'])
	timer = Timer(event_queue)
	time_interval = 60 							# Update event queue after every 60 seconds.
	listener_ = listener('a listener', event_queue, ['test1', 'test2', 'test3', 'test4', 'test5'])

	for i in ['test1', 'test2', 'test3', 'test4', 'test5']:
		event  = Event('timer', {'time': create_alarm(int(i[4])), 'etype': i})
		event_queue.new_event(event)
	
	for i in range(0, 6):
		event_queue.update()
		assert(len(listener_.record)==i)
		time.sleep(61)

	print("One listener with many alarms test passed!")
	timer.stop()

def test_one_to_one():
	event_queue = EventQueue(['timer', 'test1', 'test2', 'test3', 'test4', 'test5'])
	timer = Timer(event_queue)
	time_interval = 60 							# Update event queue after every 60 seconds.

	listeners = []
	for alarm_type in ['test1', 'test2', 'test3', 'test4', 'test5']:
		listeners.append(listener('a listener', event_queue, [alarm_type]))

	for i in ['test1', 'test2', 'test3', 'test4', 'test5']:
		event = Event('timer', {'time': create_alarm(1), 'etype': i})
		event_queue.new_event(event)
	
	event_queue.update()
	time.sleep(61)
	event_queue.update()
	
	for i in range(1, 6):
		assert(len(listeners[i-1].record) == 1)
		assert(listeners[i-1].record[0].etype == 'test'+str(i) )

	print("5 listeners with one alarm each test passed!")
	timer.stop()
	
def test_timer_stop():
	event_queue = EventQueue(['timer'])
	timer = Timer(event_queue)
	event = Event('timer', {'time': create_alarm(1), 'etype': 'test1'})
	assert(len(timer._alarm_time_queue)==0)
	timer.stop()
	timer.notify(event)
	assert(len(timer._alarm_time_queue)==1)
	time.sleep(120)
	assert(len(timer._alarm_time_queue)==1)
	
	print("Stop Test passed!")

if __name__ == '__main__':
	test_notify()
	print('test_notify() passed')
	test_timer()
	print('test_timer() passed')
	test_timer_stop()
	print('test_timer_stop() passed')
	test_one_to_many()
	print('test_one_to_many() passed')
	test_one_to_one()
	print('test_one_to_one() passed')
	print('all tests passed')
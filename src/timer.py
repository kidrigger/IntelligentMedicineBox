#!/bin/python3

"""
Timer
Simulates a timer to notify for the next medicine.
"""

import threading
from datetime import datetime, date, time
from event_queue import *

class Timer:
    _current_time = None
    _alarm_time_queue = []
    _time_interval = 0
    _event_queue = None
    _timer_stop = None
    
    # Converts time from string to datetime object.
    def _preprocess(self, alarm_time):
        today_date = date.today()
        self._current_time = datetime.now()
        alarm_time_HH_MM = alarm_time.split(':')
        HH = int(alarm_time_HH_MM[0])
        MM = int(alarm_time_HH_MM[1])
        time_obj = time(HH, MM)
        
        alarm_time = datetime.combine(today_date, time_obj) # Assume alarm is set for today at the given time.

        if alarm_time < self._current_time :                # If that time is already past, it's for tomorrow.
            alarm_time = alarm_time.replace(date=today_date.date + 1)
        return alarm_time

    def notify(self, alarm_time):
        #print("timer notified", alarm_time, self._alarm_time_queue)
        
        alarm_time.data['time'] = self._preprocess(alarm_time.data['time'])
        alarm_time = Event(alarm_time.data['etype'], alarm_time.data)
        if len(self._alarm_time_queue) == 0 :
            self._alarm_time_queue.append(alarm_time)
            return None

        i=0
        while i<len(self._alarm_time_queue) :
            if self._alarm_time_queue[i].data['time'] > alarm_time.data['time']:
                self._alarm_time_queue.insert(i, alarm_time)
                return None
            i+=1
        
        self._alarm_time_queue.append(alarm_time) # If this alarm is the furthest away one.
                

    def _wake(self):
        self._current_time = datetime.now()
        #print("timer waken up")
        #print(self._alarm_time_queue)
        i=0
        while i<len(self._alarm_time_queue) :
            next_alarm_time = self._alarm_time_queue[i]
            if self._current_time >= next_alarm_time.data['time']:   #if the time for this medicine alarm has come, notify.
                event = next_alarm_time
                #print(event)
                event.data['time'] = to_hh_mm(event.data['time'])
                self._event_queue.new_event(event)
                self._alarm_time_queue.pop(0)
            else:
                break

        if not self._timer_stop.is_set():
            # call _wake() again for the next event.
            threading.Timer(self._time_interval, self._wake, []).start()

    def stop(self):
        self._timer_stop.set()

    def _start(self):
        if self._timer_stop is None or self._timer_stop.is_set():
            self._timer_stop = threading.Event()    # This is the boolean flag to show whether the timer is on.
            self._wake()
            
    def __init__(self, event_queue):
        self._event_queue = event_queue
        event_queue.register(self, ['timer'])
        self._alarm_time_queue = []
        self._time_interval = 30                # Start the timer, and wake it now and 30 seconds hereafter
        self._start()

def to_hh_mm(datetimeobj):
    return datetimeobj.strftime('%H:%M')

def get_current_time():
    return to_hh_mm(datetime.now())

#!/bin/python3
from prescription_manager import *
from event_queue import *

def test_new_prescription():
    evq = EventQueue(['presc_man', 'timeslot'])
    pres_man = PrescriptionManager(evq)
    prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'def':[0, 0, 1, 2, 1, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    assert(len(pres_man._prescriptions)==1)
    assert(pres_man.get_prescribed_medicine(0) == {} )
    assert(pres_man.get_prescribed_medicine(1) == {'abc': 1} )
    assert(pres_man.get_prescribed_medicine(2) == {'def': 1} )
    assert(pres_man.get_prescribed_medicine(3) == {'def': 2} )
    assert(pres_man.get_prescribed_medicine(4) == {'abc': 1, 'def': 1} )
    assert(pres_man.get_prescribed_medicine(5) == {} )
    assert(pres_man.get_prescribed_medicine(6) == {'abc': 1} )
    assert(pres_man.get_prescribed_medicine(7) == {'abc': 1, 'def': 1} )

def test_del_prescription():
    evq = EventQueue(['presc_man', 'timeslot'])
    pres_man = PrescriptionManager(evq)
    prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'def':[0, 0, 1, 2, 1, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    assert(len(pres_man._prescriptions)==1)
    prescription = {'id': 2, 'medicines':{'abca':[0, 1, 1, 0, 1, 0, 3, 1], 'def1':[1, 0, 1, 0, 1, 4, 0, 1]} }
    pres_man.new_prescription(prescription)
    assert(len(pres_man._prescriptions)==2)
    prescription = {'id': 3, 'medicines':{'adbc':[2, 1, 1, 0, 1, 2, 1, 1], 'de2f':[0, 0, 3, 0, 5, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    assert(len(pres_man._prescriptions)==3)
    pres_man.delete_prescription(2)
    assert(len(pres_man._prescriptions)==2)
    assert(1 == pres_man._prescriptions[0]['id'])
    assert(3 == pres_man._prescriptions[1]['id'])
    pres_man.delete_prescription(1)
    assert(len(pres_man._prescriptions)==1)
    assert(3 == pres_man._prescriptions[0]['id'])

def test_update_prescription():
    evq = EventQueue(['presc_man', 'timeslot'])
    pres_man = PrescriptionManager(evq)
    prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'def':[0, 0, 1, 2, 1, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    prescription = {'id': 2, 'medicines':{'abca':[0, 1, 1, 0, 1, 0, 3, 1], 'def1':[1, 0, 1, 0, 1, 4, 0, 1]} }
    pres_man.new_prescription(prescription)
    prescription = {'id': 3, 'medicines':{'adbc':[2, 1, 1, 0, 1, 2, 1, 1], 'de2f':[0, 0, 3, 0, 5, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    prescription = {'id': 2, 'medicines':{'adbc':[2, 1, 1, 0, 1, 2, 1, 1], 'de2f':[0, 0, 3, 0, 5, 0, 0, 1]} }
    pres_man.update_prescription(prescription)
    assert(len(pres_man._prescriptions)==3)
    ids = [x['id'] for x in pres_man._prescriptions]
    assert(1 in ids)
    assert(2 in ids)
    assert(3 in ids)
    presc2 = None
    for x in pres_man._prescriptions:
        if x['id'] == 2:
            presc2 = x
    assert(prescription['medicines'] == presc2['medicines'])

def test_get_next_slot():
    evq = EventQueue(['presc_man', 'timeslot'])
    pres_man = PrescriptionManager(evq)
    prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 1, 0, 1, 1], 'def':[0, 0, 1, 2, 1, 0, 0, 1]} }
    pres_man.new_prescription(prescription)
    assert(pres_man.get_next_slot(0) == 1)
    assert(pres_man.get_next_slot(1) == 2)
    assert(pres_man.get_next_slot(2) == 3)
    assert(pres_man.get_next_slot(3) == 4)
    assert(pres_man.get_next_slot(4) == 6)
    assert(pres_man.get_next_slot(6) == 7)
    assert(pres_man.get_next_slot(7) == 1)

    prescription = {'id': 1, 'medicines':{'abc':[0, 1, 0, 0, 0, 0, 0, 0]} }
    pres_man.update_prescription(prescription)
    assert(pres_man.get_next_slot(0) == 1)
    assert(pres_man.get_next_slot(1) == 1)
    assert(pres_man.get_next_slot(2) == 1)
    assert(pres_man.get_next_slot(3) == 1)
    assert(pres_man.get_next_slot(4) == 1)
    assert(pres_man.get_next_slot(6) == 1)
    assert(pres_man.get_next_slot(7) == 1)





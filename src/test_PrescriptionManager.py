from PrescriptionManager import *

def test_new_prescription():
    presMan = PrescriptionManager(None)
    assert(len(presMan._prescriptions) == 0)
    prescription = {'id' : 1, 'medicine' : [1,2,3,4,5,6,7,8]}
    presMan.new_prescription(prescription)
    assert(len(presMan._prescriptions) == 1)

    print("test_new_prescription passed")

def test_delete_prescription():
    presMan = PrescriptionManager(None)
    prescription = {'id' : 1, 'medicine' : [1,2,3,4,5,6,7,8]}
    presMan.new_prescription(prescription)
    assert(len(presMan._prescriptions) == 1)
    presMan.delete_prescription(prescription)
    assert(len(presMan._prescriptions) == 0)

    print("test_delete_prescription passed")

def test_update_prescription():
    presMan = PrescriptionManager(None)
    prescription1 = {'id' : 1, 'medicine' : [1,2,3,4,5,6,7,8]}
    prescription2 = {'id' : 1, 'medicine' : [2,2,3,4,5,6,7,8]}
    presMan.new_prescription(prescription1)
    presMan.update_prescription(prescription2)
    assert(len(presMan._prescriptions) == 1)
    assert(presMan._prescriptions[0]['medicine'] == [2,2,3,4,5,6,7,8])
    
    print("test_update_prescription passed")

def test_get_next_slot():
    presMan = PrescriptionManager(None)
    val = presMan.get_next_slot(2)
    assert(val[0] == 3)
    assert(val[1] == '3')
    val = presMan.get_next_slot(8)
    assert(val[0] == 1)
    assert(val[1] == '1')
    print("test_get_next_slot passed")

def test_get_prescribed_medicine():
    presMan = PrescriptionManager(None)
    # assumed format of data in prescription {id : [{medicine : [slots] } ] }
    prescription1 = {'id':1, 'medicines': {'med1':[1,0,2,0,3,0,4,0], 'med2':[9,2,3,4,5,6,7,8]} }
    presMan.new_prescription(prescription1)
    val = presMan.get_prescribed_medicine(0)
    assert(len(val) == 2)
    print("test_get_prescribed_medicine passed")


test_new_prescription()
test_delete_prescription()
test_update_prescription()
test_get_next_slot()
test_get_prescribed_medicine()
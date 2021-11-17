from unittest import TestCase
from Calls import Calls
from ElevatorCallList import ElevatorCallList
from Node import Node
from Elevator import Elevator

class ElevatorCallList_test(TestCase):

    call1 = Calls(1.1,3,4,0,2)
    call2 = Calls(3, 8, 10, 0, 1)
    call3 = Calls(10, 5, 3, 0, 0)
    elevatorcalllist = ElevatorCallList(3)
    elevatorcalllist.add_call(call1,0,5,6)
    elevatorcalllist.add_call(call2, 1, 8, 10)
    elevatorcalllist.add_call(call3, 2, 20, 22)

    def test_add_Call(self):
        self.assertEqual(self.elevatorcalllist.upCalls[0][0].floor,3,"that the floor")
        self.assertEqual(len(self.elevatorcalllist.downCalls[0]),0)
        self.assertEqual(self.elevatorcalllist.upCalls[0][0].time_stamp,5, "check time_stamp")







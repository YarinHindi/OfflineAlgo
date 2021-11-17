from unittest import TestCase
from OffLineAlgo import OffLineAlgo
from Building import Building
from Calls import Calls
from ElevatorCallList import ElevatorCallList
from Elevator import Elevator

class OffLineAlgo_test(TestCase):
    first_Call = ("first",1.5,0,2,0,-1)
    second_Call = ("second",2.9,4,5,-1)
    callList = [first_Call,second_Call]
    algo = OffLineAlgo("B_forTest.json","Test.csv")
    for i in range(len(algo.mycall)):
        index = algo.allocate_elevator(algo.mycall[i])
        algo.mycall[i].elev_index = index

    def test_dist(self):
        self.assertEqual(self.algo.mycall[0].elev_index,1,"Need to get true for that assert cause elev 1 is faster")
        self.assertEqual(self.algo.mycall[1].elev_index,1,"Need to get true for that assert")

    def test_min_floor_max_floor(self):
        self.assertEqual(self.algo.min_floor(self.algo.callList.upCalls[1],0),2,"min floor of the two calls we are testing")
        self.assertEqual(self.algo.max_floor(self.algo.callList.upCalls[1], 0), 6,"min floor of the two calls we are testing")


    def test_existed_floor(self):
        self.assertEqual(self.algo.existed_floor(4,self.algo.callList.upCalls[1],0),(1,True),"gonna return true")










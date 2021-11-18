from unittest import TestCase
from Building import Building
from Elevator import Elevator


class Building_test(TestCase):
    elev0 = (0,100.0,-5,10,1.0,1.0,1.0,1.0)
    elev1 = (0, 50.0, -5, 10, 0.1, 0.1, 0.1, 0.1)
    elevList = [elev0,elev1]
    building = Building(-5,10,elevList)
    jsonBuilding = building.loadfromjson("B_forTest.json")

    def test_loadfromjson(self):
        self.assertEqual(len(self.building.elevatorsArray),len(self.jsonBuilding.elevatorsArray),"True")
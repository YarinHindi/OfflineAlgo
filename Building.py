from Elevator import Elevator
import json
class Building:

    def __init__(self) -> None:
        self._minFloor=0
        self._maxFloor=10
        self.elevatorsArray=[]


    def loadfromjson(self,filename):
        try:
            with open(filename,"r+") as f:
                my_d=json.load(f)
                self._minFloor=my_d["_minFloor"]
                self._maxFloor = my_d["_maxFloor"]
                allelev=my_d["_elevators"]
                for eldict in allelev:
                    elevtor = Elevator(eldict['_id'],eldict['_speed'],eldict['_minFloor'],eldict['_maxFloor']
                    ,eldict['_closeTime'],eldict['_openTime'],eldict['_startTime'],eldict['_stopTime'])
                    self.elevatorsArray.append(elevtor)

        except IOError as e:
            print(e)

    def __str__(self) -> str:
        a=""
        for i in range (0,len(self.elevatorsArray)):
            print(f" {self.elevatorsArray[i]}")
        return a








if __name__ == '__main__':
    building=Building()
    building.loadfromjson("B1.json")
    print(building)













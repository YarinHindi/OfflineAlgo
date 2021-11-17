from Elevator import Elevator
import json
class Building:

    def __init__(self,minFloor=0,maxFloor=0,elevatorsArray=[]) -> None:
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.elevatorsArray = elevatorsArray


    @staticmethod
    def loadfromjson(filename):

            with open(filename,"r+") as f:
                my_d = json.load(f)
                minFloor=my_d["_minFloor"]
                maxFloor = my_d["_maxFloor"]
                elevatorsArray=[]
                allelev=my_d["_elevators"]
                for eldict in allelev:
                    elevtor = Elevator(eldict['_id'],eldict['_speed'],eldict['_minFloor'],eldict['_maxFloor']
                    ,eldict['_closeTime'],eldict['_openTime'],eldict['_startTime'],eldict['_stopTime'])
                    elevatorsArray.append(elevtor)

                return Building(minFloor,maxFloor,elevatorsArray)

    """
    this function is static method that take a json file reprsent Building and convert him to a Building object. 
    """

    def __str__(self) -> str:
        a=""
        for i in range (0,len(self.elevatorsArray)):
            print(f" {self.elevatorsArray[i]}")
        return a

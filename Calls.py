import csv
from random import randint


class Calls:
    def __init__(self, call_time:int=0, src:int=0, dest:int=0, status:int=0, elev_index:int=-1):
        self.name = "Elevator Call"
        self.call_time = float(call_time)
        self.src = int(src)
        self.dest = int(dest)
        self.status = status
        self.elev_index = int(elev_index)
        self.time = "dt"
        self.endCall= 0


    """
    the constructor getting call time for the time which the call was requested 
    src for the source floor ,dest for the destination floor,status don't really used in the algorithm
    but can tells us what the call status and elev_index for the elevator that we will chose to allocate the call for.

    """
    @staticmethod
    def callsToCsv(arrayofCalls, output_filename):

        filename = output_filename+".csv"
        newArrayofCalls =[]
        for i in arrayofCalls:
            newArrayofCalls.append(i.__dict__.values())
        with open(filename, 'w', newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerows(newArrayofCalls)
    """
    this is static method for convert array of calls to csv file which represent the calls
    after using this function file name output.csv will be created.
    """
    @staticmethod
    def loadFromCsv(fileName):
        arr = []
        with open(fileName) as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                call = Calls(row[1], row[2], row[3], row[4], row[5])
                arr.append(call)
        return arr
    """
    this static method used to do the opposite from the function above that function will convert 
    csv file to array of call object.
    """


    def __str__(self):
        return f"Name = {self.name} time stamp={self.call_time} src={self.src} dest={self.dest} status={self.status} elevindex={self.elev_index}"
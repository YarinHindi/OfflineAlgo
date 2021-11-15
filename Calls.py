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


    @staticmethod
    def callsToCsv(arrayofCalls):

        filename = 'output.csv'
        newArrayofCalls =[]
        for i in arrayofCalls:
            newArrayofCalls.append(i.__dict__.values())
        with open(filename, 'w', newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerows(newArrayofCalls)
    @staticmethod
    def loadFromCsv(fileName):
        arr = []
        with open(fileName) as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                call = Calls(row[1], row[2], row[3], row[4], row[5])
                arr.append(call)
        return arr

    def setStatus(self, status):
        self.status = status

    def setElevator(self, elev_index):
        self.elev_index = elev_index

    def __str__(self):
        return f"Name = {self.name} time stamp={self.call_time} src={self.src} dest={self.dest} status={self.status} elevindex={self.elev_index}"

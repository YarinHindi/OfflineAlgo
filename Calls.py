import csv
class Calls:
    def __init__(self, call_time=0, src=0, dest=0, status=0, elev_index=-1):
        self.call_time = call_time
        self.src = src
        self.dest = dest
        self.status = status
        self.elev_index = elev_index

    def loadFromCsv(self, fileName):
        arr = []
        with open(fileName) as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                call = Calls(row[1], row[2], row[3])
                arr.append(call)
        return arr

    def setStatus(self, status):
        self.status = status

    def setElevator(self, elev_index):
        self.elev_index = elev_index

    def __str__(self):
        return f"time stamp={self.call_time} src={self.src} dest={self.dest} status={self.status} elevindex={self.elev_index}"

if __name__ == '__main__':
    a = Calls()
    c = a.loadFromCsv("Calls_b.csv")
    for i in c:
        print(i)
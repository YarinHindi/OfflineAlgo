import Building
import Calls
import ElevatorCallList
class Offlinealgo:

    def __init__(self,buildingjson="Building.json",callscsv="Calls.csv",outputcsv="output.csv") -> None:
        self.buildingjsons = Building.loadfromjson(("Building.json"))
        self.callscsv = Calls.loadFromCsv("Calls.csv")
        self.callList = ElevatorCallList(len(self.buildingjsons.elevatorsArray))

    def allocateElevator(self, call):
        min = 0
        index = 0
        for elev_index in range(len(self.buildingjsons.elevatorsArray)):
            current_time = self.dist(call, elev_index)
            if current_time < min:
                min = current_time
                index = elev_index
        return index

    def dist(self, call, elev_index):
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        if len(self.callList.upCalls[elev_index]) > 0 and len(self.callList.downCalls[elev_index]):
            up = 0
            down = 0
            up_index = 0
            down_index = 0
            src_time = 0
            dest_time = 0
            call_time = 0
            for i in self.callList.upCalls[elev_index]:
                if i.time_stamp < call.call_time:
                    up = i.time_stamp
                    up_index += 1
            for i in self.callList.downCalls[elev_index]:
                if i.time_stamp < call.call_time:
                    down = i.time_stamp
                    down_index += 1
            if up < down:
                way = call.dest - call.src
                otw = False
                if way > 0:
                    otw = True
                for i in range(up_index, len(self.callList.upCalls[elev_index])):
                    if otw == True:
                        if call.src > self.callList.upCalls[elev_index,i]:
                            compute = (call.src - self.callList.upCalls[elev_index][i]) / elevator._speed
                            src_time = compute + self.callList.upCalls[elev_index][i].time_stamp + elevator._stopTime + elevator._openTime
                            if src_time > call.call_time:
                                last_index = len(self.callList.upCalls[elev_index]) - 1
                                if call.dest > self.callList.upCalls[elev_index][last_index]:
                                    compute = (call.dest - self.callList.upCalls[elev_index][last_index].dest) / elevator._speed
                                    dest_time = compute + self.callList.upCalls[elev_index][last_index].time_stamp + elevator._stopTime + elevator._openTime
                                    call_time = dest_time - call.call_time

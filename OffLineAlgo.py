from Building import Building
from Calls import Calls
from ElevatorCallList import ElevatorCallList
from Elevator import Elevator
import sys


class Offlinealgo:

    def __init__(self, buliding, callscsv) -> None:
        self.buildingjsons = Building.loadfromjson(buliding)
        self.mycall=Calls.loadFromCsv(callscsv)
        self.callList = ElevatorCallList(len(self.buildingjsons.elevatorsArray))

    def allocate_elevator(self, call):
        min = sys.maxsize
        ans = ()
        for elev_index in range(len(self.buildingjsons.elevatorsArray)):
            current_time = self.dist(call, elev_index)
            if current_time[2] < min:
                min = current_time[2]
                ans = (call, elev_index, current_time[0], current_time[1])
        self.callList.add_call(ans[0], ans[1], ans[2], ans[3])
        return ans[1]

    def dist(self, call, elev_index):
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        up_index = 0
        down_index = 0
        src_time = 0
        dest_time = 0
        call_time = 0
        last_up_index = len(self.callList.upCalls[elev_index]) - 1
        last_down_index = len(self.callList.downCalls[elev_index]) - 1
        way = call.dest - call.src
        added = False
        for i in self.callList.upCalls[elev_index]:
            if i.time_stamp < call.call_time:
                up_index += 1
        if up_index > 0:
            up_index -= 1
        for i in self.callList.downCalls[elev_index]:
            if i.time_stamp < call.call_time:
                down_index += 1
        if down_index > 0:
            down_index -= 1
        if way > 0:
            src_index = up_index
            for i in range(up_index, len(self.callList.upCalls[elev_index])):
                src_index += 1
                if call.src > self.callList.upCalls[elev_index][i].floor:  # call src is on the way
                    compute = abs(call.src - self.callList.upCalls[elev_index][i].floor) / elevator.speed
                    src_time = compute + self.callList.upCalls[elev_index][i].time_stamp
                    if self.existed_floor(call.src, self.callList.upCalls[elev_index], src_index)[0] == False:
                        src_time += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    if src_time > call.call_time:  # check if the call time is on the way
                        added = True
                        if call.dest > self.max_floor(self.callList.upCalls[elev_index], src_index):  # call dest is higher than the last level call of the elevator
                            if self.existed_floor(call.src, self.callList.upCalls[elev_index], src_index)[0] == False:
                                for j in range(src_index, len(self.callList.upCalls[elev_index]) - 1):
                                    self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                            compute = abs(call.dest - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                            dest_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime
                            call_time = dest_time - call.call_time
                        else:  # call dest is lower than the highest level call of the elevator
                            dest_tup = self.existed_floor(call.dest, self.callList.upCalls[elev_index], src_index)
                            if dest_tup[0] == True:
                                dest_time = self.callList.upCalls[elev_index][dest_tup[1]]
                            else:
                                dest_index = src_index
                                for j in range(src_index, len(self.callList.upCalls[elev_index]) - 1):
                                    if call.dest > self.callList.upCalls[elev_index][j + 1].floor:
                                        dest_index += 1
                                    else:
                                        compute = abs(call.dest - self.callList.upCalls[elev_index][j].floor) / elevator.speed
                                        dest_time = compute + self.callList.upCalls[elev_index][j].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                        call_time = dest_time - call.call_time
                                        break
                                for j in range (dest_index, len(self.callList.upCalls[elev_index])):
                                    self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        break
            if added == False:
                if len(self.callList.upCalls[elev_index]) == 0:
                    if len(self.callList.downCalls[elev_index]) == 0:
                        # first call
                        compute = abs(call.src) / elevator.speed
                        src_time = compute + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    else:
                        # first up call
                        compute = abs(call.src - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                        src_time = compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                else:
                    if len(self.callList.downCalls[elev_index]) == 0:
                        compute = abs(call.src - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                        src_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    else:
                        if self.callList.upCalls[elev_index][last_up_index].time_stamp < self.callList.downCalls[elev_index][last_down_index].time_stamp:
                            compute = abs(call.src - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                            src_time = compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        else:
                            compute = abs(call.src - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                            src_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                compute = abs(call.dest - call.src) / elevator.speed
                dest_time = compute + src_time + elevator.stopTime + elevator.openTime
                call_time = dest_time - call.call_time
        else:  # the call is down
            src_index = down_index
            for i in range(down_index, len(self.callList.downCalls[elev_index])):
                src_index += 1
                if call.src < self.callList.downCalls[elev_index][i].floor:  # call src is on the way
                    compute = abs(call.src - self.callList.downCalls[elev_index][i].floor) / elevator.speed
                    src_time = compute + self.callList.downCalls[elev_index][i].time_stamp
                    if self.existed_floor(call.src, self.callList.downCalls[elev_index], src_index)[0] == False:
                        src_time += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    if src_time > call.call_time:  # check if the call time is on the way
                        added = True
                        if call.dest < self.min_floor(self.callList.downCalls[elev_index], src_index):  # call dest is lower than the last level call of the elevator
                            if self.existed_floor(call.src,self.callList.downCalls[elev_index], src_index)[0] == False:
                                for j in range(src_index, len(self.callList.downCalls[elev_index]) - 1):
                                    self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                            compute = abs(call.dest - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                            dest_time = compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime
                            call_time = dest_time - call.call_time
                        else:  # call dest is higher than the last level call of the elevator
                            dest_tup = self.existed_floor(call.dest, self.callList.downCalls[elev_index], src_index)
                            if dest_tup[0] == True:
                                dest_time = self.callList.downCalls[elev_index][dest_tup[1]]
                            else:
                                dest_index = src_index
                                for j in range(src_index, len(self.callList.downCalls[elev_index]) - 1):
                                    if call.dest < self.callList.downCalls[elev_index][j + 1].floor:
                                        dest_index += 1
                                    else:
                                        compute = abs(
                                            call.dest - self.callList.downCalls[elev_index][j].floor) / elevator.speed
                                        dest_time = compute + self.callList.downCalls[elev_index][
                                            j].time_stamp + elevator.stopTime + elevator.openTime
                                        call_time = dest_time - call.call_time
                                        break
                                for j in range(dest_index, len(self.callList.downCalls[elev_index])):
                                    self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        break
            if added == False:
                if len(self.callList.downCalls[elev_index]) == 0:
                    if len(self.callList.upCalls[elev_index]) == 0:
                        # first call
                        compute = abs(call.src) / elevator.speed
                        src_time = compute + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    else:
                        # first down call
                        compute = abs(call.src - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                        src_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                else:
                    if len(self.callList.upCalls[elev_index]) == 0:
                        compute = abs(call.src - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                        src_time = compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                    else:
                        if self.callList.downCalls[elev_index][last_down_index].time_stamp < self.callList.upCalls[elev_index][last_up_index].time_stamp:
                            compute = abs(call.src - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                            src_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        else:
                            compute = abs(call.src - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                            src_time = compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                compute = abs(call.dest - call.src) / elevator.speed
                dest_time = compute + src_time + elevator.stopTime + elevator.openTime
                call_time = dest_time - call.call_time
        my_tuple = (src_time, dest_time, call_time)
        return my_tuple

    def existed_floor(self, floor, calls, ind):
        exist = False
        index = 0
        for i in range(ind, len(calls)):
            if floor == calls[i].floor:
                exist = True
                index = calls[i].floor
        my_tup = (exist, index)
        return my_tup

    def max_floor(self, calls, ind):
        max_f = -10000
        for i in range(ind, len(calls)):
            if calls[i].floor > max_f:
                max_f = calls[i].floor
        return max_f

    def min_floor(self, calls, ind):
        min_f = 10000
        for i in range(ind, len(calls)):
            if calls[i].floor < min_f:
                min_f = calls[i].floor
        return min_f


if __name__ == '__main__':
    algo = Offlinealgo("B5.json", "Calls_d.csv")

    for i in range(len(algo.mycall)):
        index = algo.allocate_elevator(algo.mycall[i])
        algo.mycall[i].elev_index = index

    Calls.callsToCsv(algo.mycall)
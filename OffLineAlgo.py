from Building import Building
from Calls import Calls
from ElevatorCallList import ElevatorCallList
from Elevator import Elevator
import sys


class OffLineAlgo:

    def __init__(self, building, callscsv) -> None:
        self.buildingjsons = Building.loadfromjson(building)
        self.mycall = Calls.loadFromCsv(callscsv)
        self.callList = ElevatorCallList(len(self.buildingjsons.elevatorsArray))
    """
        The constructor gets two arguments ,First in the building which comes as a json file,
        we use a function that is convert the file to a Building object
        Second argument is the callcsv which comes as csv file and we use a function that convert him to
        a object that represent a array of Calls.
    """

    def existed_floor(self, floor, calls, ind):
        exist = False
        index = 0
        for i in range(ind, len(calls)):
            if floor == calls[i].floor:
                exist = True
                index = i
        my_tup = (exist, index)
        return my_tup

    """
        floor param is the floor that we going to send from dist function which tells us the floor number in the.
        calls array which we looking for to check if this floor already exist
        calls param the array of nodes we send from dist to check on if the floor existed in. 
        ind param  that pram tells us from where in the calls array to start looking for the floor if existed    
        the function return tuple with two value exist if the floor existed and index for the index 
        in the calls array that we find the floor.     
    """

    def max_floor(self, calls, ind):
        max_f = -10000
        for i in range(ind, len(calls)):
            if calls[i].floor > max_f:
                max_f = calls[i].floor
        return max_f

    """"
        :param_calls as the above function is the array of the calls 
        :parm_ind ind is the index we are stating to search in the calls array for maximum which 
        will be needed in dist function.
    """

    def min_floor(self, calls, ind):
        min_f = 10000
        for i in range(ind, len(calls)):
            if calls[i].floor < min_f:
                min_f = calls[i].floor
        return min_f

    """"
        this function do the same as the max_floor.
    """

    def allocate_elevator(self, call):
        min = sys.maxsize
        ans = ()
        for elev_index in range(len(self.buildingjsons.elevatorsArray)):
            current_time = self.dist(call, elev_index, False)
            if current_time[2] < min:
                min = current_time[2]
                ans = (call, elev_index, current_time[0], current_time[1])
        delay = self.dist(call, ans[1], True)
        self.callList.add_call(ans[0], ans[1], ans[2], ans[3])
        return ans[1]

    """"
        this function is the function that responsible for the allocation of the calls in the best 
        way this is important function for having a good and efficient allocation
        this function use the dist function for calculate the best elevator for the mission
        the function gets a call and return the elevator that going to take the mission.
    """
    def dist(self, call, elev_index, delay):
        up_index = 0
        down_index = 0
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
        tup_check = ()
        if way > 0:
            # check if the src will be "on the way" in downs
            tup_check = self.up_call_src_otw_to_down(call, up_index, down_index, elev_index, delay)
            if tup_check[0] == False:
                tup_check = self.up_call_src_otw_to_up(call, up_index, elev_index, delay)
        else:
            tup_check = self.down_call_src_otw_to_up(call, elev_index, up_index, down_index, delay)
            if tup_check[0] == False:
                tup_check = self.down_call_src_otw_to_down(call, down_index, elev_index, delay)
        my_tuple = (tup_check[1], tup_check[2], tup_check[3])
        return my_tuple
    """
        this function is the function that going to calculate the time for every elevator and after 
        the function going to calculate the times that will take each eleavtor to do the calls and who much 
        delly other call will suffer 
        the function will return tuple with three values
        first is the call time that will tells how how much times will take the calls to be served  
        second is the src time which tells us how much wll take us to get to src floor
        third is the dest time will tells us how much time will take us to get to dest
        explanation for the other 4 function will be downwards.
    """

    def up_call_src_otw_to_down(self, call, up_index, down_index, elev_index, delay):
        added = False
        src_time = 0
        dest_time = 0
        call_time = 0
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        last_up_index = len(self.callList.upCalls[elev_index]) - 1
        last_down_index = len(self.callList.downCalls[elev_index]) - 1
        if len(self.callList.downCalls[elev_index]) != 0:
            if len(self.callList.upCalls[elev_index]) != 0:
                if self.callList.downCalls[elev_index][down_index].time_stamp > self.callList.upCalls[elev_index][up_index].time_stamp:
                    # if down was the last call, then lets check if the src will enter "on the way"
                    src_index = down_index
                    if self.existed_floor(call.src, self.callList.downCalls[elev_index], down_index) == False:
                        if call.src < self.callList.downCalls[elev_index][down_index].floor:
                            for i in range(down_index, len(self.callList.downCalls[elev_index]) - 1):
                                if call.src < self.callList.downCalls[elev_index][i + 1].floor:
                                    src_index += 1
                                else:
                                    compute = abs(call.src - self.callList.downCalls[elev_index][i]) / elevator.speed
                                    src_time = compute + self.callList.downCalls[elev_index][i].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                    break
                            src_index += 1
                            if src_time > call.call_time:
                                added = True
                                for j in range(src_index, len(self.callList.downCalls[elev_index])):
                                    if self.callList.downCalls[elev_index][j].time_stamp < self.callList.upCalls[elev_index][up_index].time_stamp:
                                        src_index += 1
                                        if delay:
                                            self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                    else:
                                        break
                                src_index -= 1
                                dest_index = up_index
                                if self.existed_floor(call.dest, self.callList.upCalls[elev_index], up_index) == False:
                                    if call.dest > self.max_floor(self.callList.upCalls[elev_index], up_index):
                                        compute = abs(call.dest - self.callList.upCalls[elev_index][last_up_index]) / elevator.speed
                                        dest_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime
                                        call_time = call.call_time - dest_time
                                    else:
                                        add = 0
                                        for j in range(src_index, len(self.callList.upCalls[elev_index]) - 1):
                                            if call.dest > self.callList.upCalls[elev_index][j + 1]:
                                                add += 1
                                                dest_index += 1
                                            else:
                                                compute = abs(call.dest - self.callList.upCalls[elev_index][j]) / elevator.speed
                                                add = add * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                                                dest_time = compute + self.callList.upCalls[elev_index][j].time_stamp + elevator.stopTime + elevator.openTime + add
                                                call_time = call.call_time - dest_time
                                        dest_index -= 1
                                        if delay:
                                            for j in range(dest_index, len(self.callList.upCalls[elev_index])):
                                                self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
            else:
                # it's the first up call,
                src_index = down_index
                if self.existed_floor(call.src, self.callList.downCalls[elev_index], down_index) == False:
                    if call.src < self.callList.downCalls[elev_index][down_index].floor:
                        for i in range(down_index, len(self.callList.downCalls[elev_index]) - 1):
                            if call.src < self.callList.downCalls[elev_index][i + 1].floor:
                                src_index += 1
                            else:
                                compute = abs(call.src - self.callList.downCalls[elev_index][i]) / elevator.speed
                                src_time = compute + self.callList.downCalls[elev_index][i].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                break
                        src_index += 1
                        if src_time > call.call_time:
                            added = True
                            for j in range(src_index, len(self.callList.downCalls[elev_index])):
                                if self.callList.downCalls[elev_index][j].time_stamp < self.callList.upCalls[elev_index][up_index].time_stamp:
                                    src_index += 1
                                    if delay:
                                        self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                else:
                                    break
                            src_index -= 1
                            dest_index = up_index
                            compute = abs(call.dest - self.callList.downCalls[elev_index][src_index]) / elevator.speed
                            dest_time = compute + self.callList.downCalls[elev_index][src_index].time_stamp + elevator.stopTime + elevator.openTime
                            call_time = call.call_time - dest_time
        my_tup = (added, src_time, dest_time, call_time)
        return my_tup

    """"
    this function used as helper function for dist we have 4 case in this one we are getting UP call
    and the elevator is in state DOWN and we are going to pass the src of the call so we need to take the 
    call and do all the calculate of the the delay that will be caused 
    the function going to return tuple with 4 argument
    first added is a boolean which will tells us if this fis the case we are in if it will change is value 
    to true we know this is the case 
    src time is the time will take us ti reach src floor
    dest time same as src time
    call time time will take to end this call
    the delay argument is boolean argument that will tells us if we only going to calculate the time will 
    take us 
    and if delay value is true means we gonna calculate the time and going to add the delay to all other 
    calls that going to be delayed.
    """

    def up_call_src_otw_to_up(self, call, up_index, elev_index, delay):
        added = False
        src_time = 0
        dest_time = 0
        call_time = 0
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        last_up_index = len(self.callList.upCalls[elev_index]) - 1
        last_down_index = len(self.callList.downCalls[elev_index]) - 1
        src_index = up_index
        for i in range(up_index, len(self.callList.upCalls[elev_index])):
            src_index += 1
            if call.src > self.callList.upCalls[elev_index][i].floor:  # call src is on the way
                compute = abs(call.src - self.callList.upCalls[elev_index][i].floor) / elevator.speed
                src_time = compute + self.callList.upCalls[elev_index][i].time_stamp
                src_tup = self.existed_floor(call.src, self.callList.upCalls[elev_index], src_index)
                if src_tup[0] == False:
                    src_time += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                else:
                    src_time = self.callList.upCalls[elev_index][src_tup[1]].time_stamp
                if src_time > call.call_time:  # check if the call time is on the way
                    added = True
                    if call.dest > self.max_floor(self.callList.upCalls[elev_index],src_index):  # call dest is higher than the last level call of the elevator
                        if delay:
                            if self.existed_floor(call.src, self.callList.upCalls[elev_index], src_index)[0] == False:
                                for j in range(src_index, len(self.callList.upCalls[elev_index]) - 1):
                                    self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        compute = abs(call.dest - self.callList.upCalls[elev_index][last_up_index].floor) / elevator.speed
                        add = (len(self.callList.upCalls[elev_index]) - src_index) * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                        dest_time = compute + self.callList.upCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime + add
                        call_time = dest_time - call.call_time
                    else:  # call dest is lower than the highest level call of the elevator
                        dest_tup = self.existed_floor(call.dest, self.callList.upCalls[elev_index], src_index)
                        if dest_tup[0] == True:
                            dest_time = self.callList.upCalls[elev_index][dest_tup[1]].time_stamp
                        else:
                            dest_index = src_index
                            add = 0
                            for j in range(src_index, len(self.callList.upCalls[elev_index]) - 1):
                                if call.dest > self.callList.upCalls[elev_index][j + 1].floor:
                                    add += 1
                                    dest_index += 1
                                else:
                                    compute = abs(call.dest - self.callList.upCalls[elev_index][j].floor) / elevator.speed
                                    add = add * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                                    dest_time = compute + self.callList.upCalls[elev_index][j].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime + add
                                    call_time = dest_time - call.call_time
                                    break
                            if delay:
                                for j in range(dest_index, len(self.callList.upCalls[elev_index])):
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
        my_tup = (added, src_time, dest_time, call_time)
        return my_tup

    """"
    this function is doing the same things as the the function above 
    the different is the elevator state and in this case we are checking for the case if the 
    elevator going up and the call also UP call
    all the other things are he same as the function above.
    """
    def down_call_src_otw_to_up(self, call, elev_index, up_index, down_index, delay):
        added = False
        src_time = 0
        dest_time = 0
        call_time = 0
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        last_up_index = len(self.callList.upCalls[elev_index]) - 1
        last_down_index = len(self.callList.downCalls[elev_index]) - 1
        if len(self.callList.upCalls[elev_index]) != 0:
            if len(self.callList.downCalls[elev_index]) != 0:
                if self.callList.downCalls[elev_index][down_index].time_stamp < self.callList.upCalls[elev_index][up_index].time_stamp:
                    # if up was the last call, then lets check if the src will enter "on the way"
                    src_index = up_index
                    if self.existed_floor(call.src, self.callList.upCalls[elev_index], up_index) == False:
                        if call.src > self.callList.upCalls[elev_index][up_index].floor:
                            for i in range(up_index, len(self.callList.upCalls[elev_index]) - 1):
                                if call.src > self.callList.upCalls[elev_index][i + 1].floor:
                                    src_index += 1
                                else:
                                    compute = abs(call.src - self.callList.upCalls[elev_index][i]) / elevator.speed
                                    src_time = compute + self.callList.upCalls[elev_index][i].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                    break
                            src_index += 1
                            if src_time > call.call_time:
                                added = True
                                for j in range(src_index, len(self.callList.upCalls[elev_index])):
                                    if self.callList.upCalls[elev_index][j].time_stamp < self.callList.downCalls[elev_index][up_index].time_stamp:
                                        src_index += 1
                                        if delay:
                                            self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                    else:
                                        break
                                src_index -= 1
                                dest_index = down_index
                                if self.existed_floor(call.dest, self.callList.downCalls[elev_index],down_index) == False:
                                    if call.dest < self.min_floor(self.callList.downCalls[elev_index], down_index):
                                        compute = abs(call.dest - self.callList.downCalls[elev_index][last_down_index]) / elevator.speed
                                        dest_time = compute + self.callList.downCalls[elev_index][last_up_index].time_stamp + elevator.stopTime + elevator.openTime
                                        call_time = call.call_time - dest_time
                                    else:
                                        add = 0
                                        for j in range(down_index, len(self.callList.downCalls[elev_index]) - 1):
                                            if call.dest < self.callList.downCalls[elev_index][j + 1]:
                                                add += 1
                                                dest_index += 1
                                            else:
                                                compute = abs(call.dest - self.callList.downCalls[elev_index][j]) / elevator.speed
                                                add = add * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                                                dest_time = compute + self.callList.downCalls[elev_index][j].time_stamp + elevator.stopTime + elevator.openTime + add
                                                call_time = call.call_time - dest_time
                                        dest_index -= 1
                                        if delay:
                                            for j in range(dest_index, len(self.callList.downCalls[elev_index])):
                                                self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
            else:
                # if up was the last call, then lets check if the src will enter "on the way"
                src_index = up_index
                if self.existed_floor(call.src, self.callList.upCalls[elev_index], up_index) == False:
                    if call.src > self.callList.upCalls[elev_index][up_index].floor:
                        for i in range(up_index, len(self.callList.upCalls[elev_index]) - 1):
                            if call.src > self.callList.upCalls[elev_index][i + 1].floor:
                                src_index += 1
                            else:
                                compute = abs(call.src - self.callList.upCalls[elev_index][i]) / elevator.speed
                                src_time = compute + self.callList.upCalls[elev_index][i].time_stamp + elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                break
                        src_index += 1
                        if src_time > call.call_time:
                            added = True
                            for j in range(src_index, len(self.callList.upCalls[elev_index])):
                                if self.callList.upCalls[elev_index][j].time_stamp < self.callList.downCalls[elev_index][up_index].time_stamp:
                                    src_index += 1
                                    if delay:
                                        self.callList.upCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                                else:
                                    break
                            src_index -= 1
                            dest_index = down_index
                            compute = abs(call.dest - self.callList.upCalls[elev_index][src_index]) / elevator.speed
                            dest_time = compute + self.callList.upCalls[elev_index][src_index].time_stamp + elevator.stopTime + elevator.openTime
                            call_time = call.call_time - dest_time
        my_tup = (added, src_time, dest_time, call_time)
        return my_tup
    """"
    this function is symmetrical to the function above
    is the opposite for the function up_call_src_otw_to_down.
    """
    def down_call_src_otw_to_down(self, call, down_index, elev_index, delay):
        added = False
        src_time = 0
        dest_time = 0
        call_time = 0
        elevator = self.buildingjsons.elevatorsArray[elev_index]
        last_up_index = len(self.callList.upCalls[elev_index]) - 1
        last_down_index = len(self.callList.downCalls[elev_index]) - 1
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
                    if call.dest < self.min_floor(self.callList.downCalls[elev_index],src_index):  # call dest is lower than the last level call of the elevator
                        if delay:
                            if self.existed_floor(call.src, self.callList.downCalls[elev_index], src_index)[0] == False:
                                for j in range(src_index, len(self.callList.downCalls[elev_index]) - 1):
                                    self.callList.downCalls[elev_index][j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
                        add = 0
                        src_tup = self.existed_floor(call.src, self.callList.downCalls[elev_index], src_index)
                        if src_tup[0] == False:
                            for j in range(src_index, len(self.callList.downCalls[elev_index]) - 1):
                                add += 1
                        else:
                            src_time = self.callList.downCalls[elev_index][src_tup[1]].time_stamp
                        compute = abs(call.dest - self.callList.downCalls[elev_index][last_down_index].floor) / elevator.speed
                        add = add * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                        dest_time = add + compute + self.callList.downCalls[elev_index][last_down_index].time_stamp + elevator.stopTime + elevator.openTime
                        call_time = dest_time - call.call_time
                    else:  # call dest is higher than the last level call of the elevator
                        dest_tup = self.existed_floor(call.dest, self.callList.downCalls[elev_index], src_index)
                        if dest_tup[0] == True:
                            dest_time = self.callList.downCalls[elev_index][dest_tup[1]].time_stamp
                        else:
                            dest_index = src_index
                            add = 0
                            for j in range(src_index, len(self.callList.downCalls[elev_index]) - 1):
                                if call.dest < self.callList.downCalls[elev_index][j + 1].floor:
                                    add += 1
                                    dest_index += 1
                                else:
                                    compute = abs(call.dest - self.callList.downCalls[elev_index][j].floor) / elevator.speed
                                    add = add * (elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime)
                                    dest_time = add + compute + self.callList.downCalls[elev_index][j].time_stamp + elevator.stopTime + elevator.openTime
                                    call_time = dest_time - call.call_time
                                    break
                            if delay:
                                for j in range(dest_index, len(self.callList.downCalls[elev_index])):
                                    self.callList.downCalls[elev_index][
                                        j].time_stamp += elevator.stopTime + elevator.openTime + elevator.closeTime + elevator.startTime
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
        my_tup = (added, src_time, dest_time, call_time)
        return my_tup

    """"
      this function is symmetrical to the function above
      is the opposite for the function up_call_src_otw_to_up.
    """
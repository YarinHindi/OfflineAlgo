import Node


class ElevatorCallList:

    def __init__(self, num_of_elevators):
        upCalls = []
        for i in range(0, num_of_elevators):
            upCalls.append([])
        downCalls = []
        for i in range(0, num_of_elevators):
            downCalls.append([])

    def addCall(self, call, elev_index, src_time, dest_time):
        way = call.dest - call.src
        src_node = Node(call.src, src_time)
        dest_node = Node(call.dest, dest_time)
        if way > 0:
            self.upCalls[elev_index].append(src_node)
            self.upCalls[elev_index].append(dest_node)
            self.upCalls = self.sort(self.upCalls, elev_index)
        else:
            self.downCalls[elev_index].append(src_node)
            self.downCalls[elev_index].append(dest_node)
            self.downCalls = self.sort(self.downCalls, elev_index)

    def sort(self, calls, elev_index):
        n = len(calls[elev_index])
        # Traverse through all array elements
        for i in range(n - 1):
            # range(n) also work but outer loop will repeat one time more than needed.

            # Last i elements are already in place
            for j in range(0, n - i - 1):

                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if calls[j].time_stamp > calls[j + 1].time_stamp:
                    calls[j], calls[j + 1] = calls[j + 1], calls[j]
        return calls
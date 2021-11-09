class Node:

    def __init__(self, floor, time_stamp):
        self.floor = floor
        self.time_stamp = time_stamp

    def __str__(self):
        return "floor ",self.floor,", time stamp: ",self.time_stamp
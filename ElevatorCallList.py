class ElevatorCallList:

    def __init__(self):
        upCalls = []
        downCalls = []
        tempCalls = []

    def addCall(self, call, isTemp):
        if isTemp:
            self.tempCalls.append(call)
        else:
            way = call.dest - call.src
            if way > 0:
                self.upCalls.append(call)
            else:
                self.downCalls.append(call)

    def tempCheck(self, call):
        return False
#   returm true or false
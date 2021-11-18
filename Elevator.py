class Elevator:

    def __init__(self,id,speed,minfloor,maxfloor,closetime,openttime,starttime,stoptime) -> None:
        self.id = id
        self.speed = speed
        self.minFloor = minfloor
        self.maxFloor = maxfloor
        self.closeTime = closetime
        self.openTime = openttime
        self.startTime = starttime
        self.stopTime = stoptime


    def __str__(self) -> str:
        return f"id={self.id} speed={self.speed} minfloor={self.minFloor} maxfloor={self.maxFloor} closetime={self.closeTime} opentime={self.openTime}" \
               f" starttime={self.startTime} stoptime={self.stopTime}"
class Elevator:

    def __init__(self,id,speed,minfloor,maxfloor,closetime,openttime,starttime,stoptime) -> None:
        self._id=id
        self._speed=speed
        self._minFloor=minfloor
        self._maxFloor=maxfloor
        self._closeTime=closetime
        self._openTime=openttime
        self._startTime=starttime
        self._stopTime=stoptime


    def __str__(self) -> str:
        return f"id={self._id} speed={self._speed} minfloor={self._minFloor} maxfloor={self._maxFloor} closetime={self._closeTime} opentime={self._openTime}" \
               f" starttime={self._startTime} stoptime={self._stopTime}"




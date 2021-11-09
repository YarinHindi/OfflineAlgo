import Building
import Calls
class Offlinealgo:

    def __init__(self,buildingjson="Building.json",callscsv="Calls.csv",outputcsv="output.csv") -> None:
        self.buildingjsons = Building.loadfromjson(("Building.json"))
        self.callscsv = Calls.loadFromCsv("Calls.csv")

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

        return 0

import sys
from OffLineAlgo import OffLineAlgo
from Calls import Calls

"""
in the main function we are creating a OffLineAlgo object and we are getting a json file represent 
object Building and csv file represent all the calls we are getting.

the for loop will run on the length of the calls array and for each call we going to send to 
the allocate function that will return us the index representing the elevator that will take the call
after we are going to finish we are going to used the function that convert the calls array to csv 
file and in the file we have the answer for which elevator will take each call.
"""
if __name__ == '__main__':
    algo = 0
    output_filename = ""
    if len(sys.argv) == 4:
        try:
            building_filename = sys.argv[1]
            calls_filename = sys.argv[2]
            output_filename = sys.argv[3]
            algo = OffLineAlgo(building_filename, calls_filename)
        except:
            print("Wrong building or calls file path.\n")
    else:
        while True:
            try:
                building_filename = input("json building file name (path): ")
                calls_filename = input("csv calls file name (path): ")
                algo = OffLineAlgo(building_filename, calls_filename)
                output_filename = input("output file name: ")
                break
            except:
                print("Wrong files path.\n")
                continue
    for i in range(len(algo.mycall)):
        index = algo.allocate_elevator(algo.mycall[i])
        algo.mycall[i].elev_index = index
    Calls.callsToCsv(algo.mycall, output_filename)
    print("New csv file has been created named: "+output_filename)
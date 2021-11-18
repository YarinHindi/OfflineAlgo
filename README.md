# OfflineAlgo
In this task we were required to create an offline algorithm of smart elevators.
We were given some excel files that present elevators calls, and some json's files that present buildings.
In this algorithm we calculated the best optimal elevators for all of the calls.

# Algorithm logic
The algorithm logic is based on the following:
1) For each call, the fastest elevator that will end the call (relative to the calls that the elevator already has) will be chosen.
2) For each call, the algorithm will check if the call is "on the way", meaning that we dont won't to add the call at the end of the elevators calls.
3) After each call add, we are sorting the elevators calls by time stamps.
4) We will start adding calls one by one to the elevators by computing the best optimal track for each elevator.
5) As our teacher decided, if an elevator has now an up call, the elevator will keep doing up calls (only if the elevator doesn't need to change direction for that call), same for down calls.
6) You can find a more detailed explanation for each function in the documentation.


# Project structure
Class name | description
--- | ---
main | The main class of the program that runs the whole proccess.
OfflineAlgo | The algorithm itself, calculating the optimal elevators track for all of the calls.
ElevatorCallList | The class that holds each elevator calls.
Node | Each call that we entered in ElevatorCallList object, is a Node type who has a floor value, and a time stamp value.
Elevator | Demonstrate an elevator, and has all the variables that are needed to operate.
Building | Demonstrate a building, has a list of elevators, min and max floor.
Calls | Demonstrate a call for elevator, and has all the variables that are needed for calculation.

# Simulation results
Building | Case | Average waiting time per call | Uncompleted calls
--- | --- | --- | ---
B1 | a | 112.92 | 0
B2 | a | 46.19 | 0
B3 | a | 29.57 | 0
B3 | b | 533.69 | 239
B3 | c | 538.05 | 189
B3 | c | 518.05 | 127
B4 | a | 19.93 | 0
B4 | b | 191.63 | 7
B4 | c | 187.94 | 2
B4 | d | 182.68 | 0
B5 | a | 16.45 | 0
B5 | b | 34.58 | 0
B5 | c | 34.27 | 0
B5 | d | 35.21 | 0

# UML
![image](https://user-images.githubusercontent.com/63747865/142415833-bb936e41-a932-40f3-b844-48494b788fc0.png)

# How to run
Run the main.py file, with the right json file that present building and csv file that present calls.
Template for running the algorithm:

python main.py <building json> <calls csv> <output file name>


Example for running the algorithm:

python main.py Buildings//B3.json Calls//Calls_c.csv output

Template for running the test simulation:

java -jar Ex1_checker_V1.2_obf.jar <Id's> <building json> <calls csv> <output file name>


Example for running the test simulation:

java -jar Ex1_checker_V1.2_obf.jar 12345 B3.json Calls_c.csv output.log


# project creators
Matan Yarin Shimon & Yarin Hindi
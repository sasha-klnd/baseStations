import sys
import json
import os

def main(data):
    # Welcome message
    print("Welcome to the Base Stations Statistics Viewer!")
    menuSelect = 1
    subMenuSelect = 1

    # While loop for processing repeated menu interactions
    while menuSelect != 4:
        printMenu()

        menuSelect = input("\nEnter your choice: ")
        try:
            # Try to convert the input to a valid integer
            menuSelect = int(menuSelect)
        except ValueError:
            print("You must enter a valid number.\n")
            continue
        
        if menuSelect < 1 or menuSelect > 4:
            print("You must enter a valid number.\n")
            continue

        if menuSelect == 1:
            displayGlobalStatistics(data)
            printDivider()
            continue
        elif menuSelect == 2:
            while subMenuSelect != 3:
                print("\nPlease select the next option.")
                printSubMenu()
                subMenuSelect = input("\nEnter your choice: ")

                try:
                    # Try to convert the input to a valid integer
                    subMenuSelect = int(subMenuSelect)
                except ValueError:
                    print("You must enter a valid number.\n")
                    continue
                
                if subMenuSelect == 1:
                    continue
                elif subMenuSelect == 2:
                    continue
                elif subMenuSelect == 3:
                    print("Returning to main menu.\n")
                    printDivider()
                    break
            continue
        elif menuSelect == 3:
            continue

    print("\nExiting the program. Goodbye.\n")
    return

# String for displaying the main menu
def printMenu():
    print('''
1.  Display Global Statistics
2.  Display Base Station Statistics
        2.1.  Statistics for a random station
        2.2.  Choose a station by ID
3.  Check Coverage
4.  Exit''')
    return

# String for displaying the sub-menu if user picks 2
def printSubMenu():
    print('''1.  Statistics for a random station
2.  Choose a station by ID
3.  Return to main menu''')
    return

# Prints a divider line across the terminal
def printDivider():
    terminal_size = os.get_terminal_size()
    print('-' * terminal_size.columns)
    return

def displayGlobalStatistics(data):
    print()
    baseStations = data.get("baseStations")

    totalStations = len(baseStations)

    totalAnts = 0
    for station in baseStations:
        totalAnts += len(station.get("ants"))

    maxAntennas = 0
    for station in baseStations:
        if len(station.get("ants")) > maxAntennas:
            maxAntennas = len(station.get("ants"))
    
    minAntennas = maxAntennas
    for station in baseStations:
        if len(station.get("ants")) < minAntennas:
            minAntennas = len(station.get("ants"))

    avgAntennas = totalAnts / totalStations

    # For both of these values, +1 is added since the first "square" is covered too
    squaresCoveredLat = (data.get("max_lat") - data.get("min_lat") + 1) / data.get("step")
    squaresCoveredLon = (data.get("max_lon") - data.get("min_lon") + 1) / data.get("step")
    squaresCovered = squaresCoveredLat * squaresCoveredLon

    uniqueCoveragePts = []
    multCoveragePts = []

    for station in baseStations:
        for ant in station.get("ants"):
            for point in ant.get("pts"):
                if point in uniqueCoveragePts:
                    multCoveragePts.append(point)
                elif (point not in uniqueCoveragePts) and (point not in multCoveragePts):
                    uniqueCoveragePts.append(point)

    print("Total number of base stations for this provider: {}".format(totalStations))
    print("Total number of antennas across all stations: {}".format(totalAnts))
    print("The max, min, and average number of antennas per station: {}, {}, {}".format(maxAntennas, minAntennas, avgAntennas))
    print("Total number of points covered by exactly one antenna: {}".format(len(uniqueCoveragePts)))


    print()
    return

# Basic checking to ensure command line arguments are valid
argc = len(sys.argv)
# if argc > 2:
#     print("Too many arguments provided. Only provide one additional argument in the form of a .json file.")
#     exit(1)
# elif argc < 2:
#     print("ERROR: You must include a .json file to run this program.")
#     exit(1)


# fileName = sys.argv[1]

fileName = "test.json"

if "." not in fileName:
    print("Invalid file name: missing file type extension.")
    exit(2)
elif ".json" not in fileName:
    print("Invalid file name: file argument must be .json file.")
    exit(3)
else:
    # Open the file and read into a dictionary
    with open(fileName, "r") as f:
        data = json.load(f)

main(data)
from math import pi
from math import floor
from math import log10

AIR_DENSITY : float = 1.2 # Kilograms per cubic meter
NUMERIC_CHARS = ['0','1','2','3','4','5','6','7','8','9']
                           
bladeLength : float # Meters
avgWindSpeed : float # Meters per second
operatingEfficiency : float # Percentage 0-100

windmillEnergyProduction : float # Watts

userInput : str

def listHasStringValue(array:list[str],value:str) -> bool:

    item : str
    for item in array:

        if item == value:
            return True

    return False

def isStringValidFloat(string:str) -> bool:

    hasPeriod : bool = False
    i : int = 0

    char : str
    for char in string:

        if listHasStringValue(NUMERIC_CHARS,char): # if letter is numeric
            pass

        else:

            if char == '-':

                if i == 0:
                    pass # leading '-' allowed

                else:
                    return False # '-' in body not allowed

            elif char == '.':

                if hasPeriod:
                    return False # more than one period not allowed

                else:
                    hasPeriod = True # one period allowed

            else:
                return False # no other chars accepted
            
        i += 1

    return True

def isStringValidPercentage(string:str) -> bool:

    if string[len(string)-1] == '%':
        string = string.replace('%','')

    return isStringValidFloat(string)

# parameter 'bladelen' named this way to avoid confusion with global 'bladeLength'
def getWindmillMaximumEnergyProduction(windspeed:float,bladelen:float) -> float:
    return 0.6 * (pi * (bladelen ** 2)) * (windspeed ** 3)

# efficiency must be between 0 and 100
# parameter 'bladelen' named this way to avoid confusion with global 'bladeLength'
def getWindmillActualEnergyProduction(windspeed:float,bladelen:float,efficiency:float) -> float:

    if efficiency < 0 or efficiency > 100:
        print("ERROR: at line 50 in getWindmillActualEnergyProduction, parameter 'efficiency' out of range\n")
        return -1

    return getWindmillMaximumEnergyProduction(windspeed,bladelen) * (efficiency / 100)

def getOrderOfMagnitude(x:float)->int:
    return floor(log10(x))

def formatWattage(value:float) -> dict: # return dict {power:float,unit:char}

    return {'power':value,'unit':''}

# using main function just for cohesion
def main():

    print("-- welcome to the Windmill Power Output calculator --\n")

    while True:

        # handle blade length
        print("\nWindmill blade length? (In meters, only numbers, no fractions)")
        while True:
            userInput = input()

            if isStringValidFloat(userInput):
                bladeLength = float(userInput)
                break

            else:
                print("Invalid input (Only numbers, no fractions)\n")

        # handle average wind speed
        print("\nWhat is the average wind speed where this windmill is located? (In meters per second, only numbers, no fractions)")
        while True:
            userInput = input()

            if isStringValidFloat(userInput):
                avgWindSpeed = float(userInput)
                break

            else:
                print("Invalid input (Only numbers, no fractions)\n")

        # handle operating efficiency
        print("\nWhat is the windmill's operating efficiency percentage? (As a percentage, between 0% and 100%)")
        while True:
            userInput = input()

            if isStringValidPercentage(userInput):
                userInput = userInput.replace('%','')
                operatingEfficiency = float(userInput)

                if operatingEfficiency > 100 or operatingEfficiency < 0:
                    print("Value out of range (0-100)\n")

                else:
                    break

            else:
                print("Invalid input (Only numbers, no fractions)\n")

        # get result and output
        windmillEnergyProduction = getWindmillActualEnergyProduction(avgWindSpeed,bladeLength,operatingEfficiency)
        print("\nWindmill Power Output: {power}{unit}W\n".format(power = windmillEnergyProduction, unit = ''))

        # handle repeat / termination
        userInput = input("\n\n -- enter to continue, input e to exit --\n\n")
        if userInput == "e":
            break

main()
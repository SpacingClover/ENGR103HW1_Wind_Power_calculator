#######################################################################
# Program Filename: ENGR103HW1_Wind_Power_calculatory.py
# Author: Dominic Duncan
# Date: 4/10/25
# Description: Termial program to calculate the power output of a windmill
# Input: Windmill attributes such as blade length, operating efficiency, average wind speed
# Output: Windmill power output
#######################################################################

from math import pi
from math import floor
from math import ceil
from math import log10

AIR_DENSITY : float = 1.2 # Kilograms per cubic meter
NUMERIC_CHARS : list[str] = ['0','1','2','3','4','5','6','7','8','9']
MAGNITUDE_UNITS : list[str] = ['p','n','𝜇','m','','k','M','G','T']

#######################################################################
# Function: list_has_string_value
# Description: checks if a string list has a specific string value
# Parameters: array:list[str], value:str
# Return values: boolean
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def list_has_string_value(array:list[str],value:str) -> bool:

    item : str
    for item in array:

        if item == value:
            return True

    return False

#######################################################################
# Function: is_string_valid_float
# Description: checks if inputted string can be converted to a float
# Parameters: string:str
# Return values: boolean
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def is_string_valid_float(string:str) -> bool:

    has_period : bool = False
    i : int = 0

    if len(string) == 0:
        return False

    char : str
    for char in string:

        if list_has_string_value(NUMERIC_CHARS,char): # if letter is numeric
            pass

        else:

            if char == '-':

                if i == 0:
                    pass # leading '-' allowed, so that user can recieve more applicable 'out of bounds' message later on

                else:
                    return False # '-' in body not allowed

            elif char == '.':

                if has_period:
                    return False # more than one period not allowed

                else:
                    has_period = True # one period allowed, decimal place

            else:
                return False # no other chars accepted
            
        i += 1

    return True

#######################################################################
# Function: is_string_valid_percentage
# Description: checks a string if it can be converted to a float, but allows a '%' character at the end
# Parameters: string:str
# Return values: boolean
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def is_string_valid_percentage(string:str) -> bool:

    if len(string) == 0:
        return False

    if string[len(string)-1] == '%':
        string = string.replace('%','')

    return is_string_valid_float(string)

#######################################################################
# Function: get_windmill_maximum_energy_production
# Description: calculate the maximum windmill output Wattage
# Parameters: windspeed:float, bladelen:float
# Return values: float
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

# parameter 'bladelen' named this way to avoid confusion with global 'bladeLength'
def get_windmill_maximum_energy_production(windspeed:float,bladelen:float) -> float:
    return 0.6 * (pi * (bladelen ** 2)) * (windspeed ** 3)

#######################################################################
# Function: get_windmill_actual_energy_production
# Description: calculate the windmill's REAL output Wattage
# Parameters: windspeed:float, bladelen:float, efficiency:float
# Return values: float
# Pre-Conditions: efficiency must be between 0 and 100%
# Post-Conditions: None
#######################################################################

# efficiency must be between 0 and 100
# parameter 'bladelen' named this way to avoid confusion with global 'bladeLength'
def get_windmill_actual_energy_production(windspeed:float,bladelen:float,efficiency:float) -> float:

    if efficiency < 0 or efficiency > 100:
        print("ERROR: in get_windmill_actual_energy_production, parameter 'efficiency' out of range\n")
        return -1

    return get_windmill_maximum_energy_production(windspeed,bladelen) * (efficiency / 100)

#######################################################################
# Function: get_order_of_magnitude
# Description: given a float, find the order of magnitude of it's highest value
# Parameters: x:float
# Return values: integer
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def get_order_of_magnitude(x:float) -> int:

    if x == 0:
        print("ERROR: in get_order_of_magnitude, parameter 'x' cannot be 0")
        return 0

    return floor(log10(x))

#######################################################################
# Function: get_highest_place
# Description: given a float, get the 'place' of it's highest value, where the ones place = 1
# Parameters: x:float
# Return values: integer
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def get_highest_place(x:float) -> int:

    return get_order_of_magnitude(x)+1

#######################################################################
# Function: round_up_to_step
# Description: round 'num' up to nearest multiple of 'step'
# Parameters: num:float, step:int
# Return values: integer
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def round_up_to_step(num:float,step:int) -> int:

    return ceil(num / step) * step

#######################################################################
# Function: format_wattage
# Description: Take power in watts, reformat for best magnitude units
# Parameters: watts : Float
# Return values: Returns format mapping dictionary compatible with output string template
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def format_wattage(watts:float) -> dict:

    #convert wattage to three-place magnitude index from zero
    idx : int = floor((round_up_to_step(get_highest_place(watts),3)/3)-1)

    # clamp unit character index to remain in range of MAGNITUDE_UNITS
    if idx < -4: idx = -4
    elif idx > 4: idx = 4

    # change magnitude to respect new units
    value : float = watts * (1000**(-idx))

    # shift forward so that negative magnitudes are not negative indices
    idx += 4

    return {'value':value,'unit':MAGNITUDE_UNITS[idx]}

#######################################################################
# Function: get_float_input
# Description: prompt the user with inputMessage string, repeat until user gives valid input, return input as float
# Parameters: inputMessage:str, acceptPercentage:bool
# Return values: float
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################

def get_float_input(inputMessage:str,acceptPercentage:bool=False) -> float:

    user_input : str
    result : float

    print(inputMessage)

    while True:
        user_input = input()

        if acceptPercentage:

            if is_string_valid_percentage(user_input):
                user_input = user_input.replace('%','')
                result = float(user_input)

                if result > 100 or result <= 0:
                    print("Value out of range (0 < x ≤ 100)\n")

                else:
                    break

            else:
                print("Invalid input (Only numbers, no fractions)\n")
                
        else: # normal floats

            if is_string_valid_float(user_input):
                result = float(user_input)

                if result <= 0:
                    print("Value out of range (0 < x)\n")

                else:
                    break

            else:
                print("Invalid input (Only numbers, no fractions)\n")

    return result

def main():

    blade_length : float # Meters
    avg_wind_speed : float # Meters per second
    operating_efficiency : float # Percentage 0-100
    user_input : str
    windmill_energy_production : float # Watts

    print("-- welcome to the Windmill Power Output calculator --\n")

    while True:
        
        # get blade length
        blade_length = get_float_input("\nWindmill blade length? (In meters, only numbers, no fractions)")

        # get average wind speed
        avg_wind_speed = get_float_input("\nWhat is the average wind speed where this windmill is located? (In meters per second, only numbers, no fractions)")

        # get operating efficiency
        operating_efficiency = get_float_input("\nWhat is the windmill's operating efficiency percentage? (As a percentage, between 0% and 100%)",True)

        # calculate result
        windmill_energy_production = get_windmill_actual_energy_production(avg_wind_speed,blade_length,operating_efficiency)

        # format and print output message
        print("\nWindmill Power Output: {value} {unit}W\n".format_map(format_wattage(windmill_energy_production)))

        # handle repeat / termination
        user_input = input("\n\n -- enter to continue, input e to exit --\n\n")
        if len(user_input) > 0 and user_input[0] == "e": # only checking first char in case they wrote "exit", "egress", or "escaparse"
            break

main()
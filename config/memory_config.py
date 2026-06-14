from typing import Any
import config.config as config
import logging
logging.basicConfig(level=logging.ERROR)
from colorama import init, Fore # type: ignore
import sys
# for suppressing python traceback
sys.tracebacklimit = 0 

# set memory function allocate space for var to store data
def set_memory(variable : str, value : Any):
    
    config.local_memory[variable] = value

# get memory fetches data from the db and returns it if founded
def get_memory(variable : str):
    # use try and catch to bypass key error tht we might encounter
    try:
        # try to return the data if its not none
        if config.local_memory[variable] != None:
            return config.local_memory[variable].format(**config.local_memory)
    
    # catch Key error and stop the program
    except KeyError as e:
        # halts the program by turning the main switch off
        config.isError = True
        # displaying the error for witch var wasn't able to fetch data is about
        logging.error(Fore.RED+f" No variable declared in '\033[4m\033[1m{variable}\033[0m"+Fore.RED+"' name")
        # returning none for safety
        return None
        
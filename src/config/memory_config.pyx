from typing import Any
import config.config as config
import logging
logging.basicConfig(level=logging.ERROR)
import cython as c
from colorama import init, Fore # type: ignore
import sys
# for suppressing python traceback
sys.tracebacklimit = 0 
from modules.data_node import DataModule # type: ignore

@c.wraparound(False)
@c.boundscheck(False)
# set memory function allocate space for var to store data
def set_memory(variable : str, value : Any, scope=None):
    data_object: DataModule = DataModule(variable, value)
    config.local_memory[variable if scope == None else scope+variable] = data_object


@c.wraparound(False)
@c.boundscheck(False)
# get memory fetches data from the db and returns it if founded
def get_memory(variable : str, scope=None):
    # use try and catch to bypass key error tht we might encounter
    try:
        if variable in config.local_memory:
            scope = None
        # try to return the data if its not none
        if config.local_memory[variable if scope == None else scope+variable] != None:
            data_object: DataModule = config.local_memory[variable if scope == None else scope+variable]
            value= data_object.data
            if type(value) is str and "REPLACE64@9" in value:
                fetch_var = config.local_memory[variable.format(**config.local_memory)].data
                exe_rub =  config.local_memory[str(fetch_var)[1:-1]].data
                return exe_rub
            elif type(value) is str:
                if value[0] == '~':
                    return value[1 :]
                else:
                    return value.format(**config.local_memory)
            else: return value
    
    # catch Key error and stop the program
    except KeyError :
        # halts the program by turning the main switch off
        config.isError = True
        # displaying the error for witch var wasn't able to fetch data is about
        logging.error(Fore.RED+f" No variable declared in '\033[4m\033[1m{variable}\033[0m"+Fore.RED+"' name")
        # returning none for safety
        return None
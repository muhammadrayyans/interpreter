from typing import Any
import config.config as config
import logging
logging.basicConfig(level=logging.ERROR)
from colorama import init, Fore # type: ignore
import sys
# for suppressing python traceback
sys.tracebacklimit = 0 
from modules.data_node import DataModule # type: ignore

# set memory function allocate space for var to store data
def set_memory(variable : str, value : Any):
    print(f'Memory tree - from {variable} to {value}')
    data_object = DataModule(variable, value)
    config.local_memory[variable] = data_object

# get memory fetches data from the db and returns it if founded
def get_memory(variable : str):
    # use try and catch to bypass key error tht we might encounter
    try:
        # try to return the data if its not none
        if config.local_memory[variable] != None:
            data_object: DataModule = config.local_memory[variable]
            _, value, _ = data_object.execute()
            if type(value) is str:
                if value[0] == '~':
                    return value[1 :]
                else:
                    if '<data_node.DataModule' in value.format(**config.local_memory):
                        value  = value.replace('{', '')
                        value = value.replace('}', '')
                        if config.local_memory[value].data != 'REPLACE64@9':
                            return config.local_memory[value].data
                        else: return value
                    elif value.format(**config.local_memory) :
                        return value.format(**config.local_memory)
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
        
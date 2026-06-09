from utils import debug
import config

# set memory function allocate space for var to store data
def set_memory(variable : str, value : any):
    config.local_memory[variable] = value

# get memory fetches data from the db and returns it if founded
def get_memory(variable : str):
    
    # use try and catch to bypass key error tht we might encounter
    try:
        # try to return the data if its not none
        if config.local_memory[variable] != None:
            return config.local_memory[variable]
    
    # catch Key error and stop the program
    except KeyError as e:
        # halts the program by turning the main switch off
        config.isError = True
        # displaying the error for witch var wasn't able to fetch data is about
        print(f"Error no variable declared in '{variable}' name")
        # returning none for safety
        return None
        
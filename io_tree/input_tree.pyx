from config.config import DataType, local_memory
from config.memory_config import set_memory, get_memory
import logging
logger = logging.getLogger(' input')
logger.setLevel(logging.DEBUG)
from typing import Any
import cython as c
from modules.data_node import DataModule
from modules.get_parser import GetParser

class Get:
    """A class that helps to get user input
    
    Args:
        var_name: name of var witch data is going to be stored
        print_data: data that is going to be printed
        isConverted: decides if the data should be converted to another type
        dtype: the type witch to be converted if isConverted turns out to be true
    """
    
    def __init__(self,object: GetParser):
        self.object = object
        self.dtype: Any
        
    @c.boundscheck(False)  
    @c.wraparound(False)    
    def execute(self):
        var_name, print_data, isConverted, dtype = self.object.execute()
        self.dtype = dtype
        if print_data != None:
            print(print_data, end="")
        value: str = input()
        data_obj: DataModule = local_memory[f'{var_name}REPLACE64@9']
        data_obj.value_change(value, isConverted)

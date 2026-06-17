from config.config import DataType, local_memory
from config.memory_config import set_memory, get_memory
import logging
logger = logging.getLogger(' input')
logger.setLevel(logging.DEBUG)
from typing import Any
import cython as c
from modules.data_node import DataModule

class Get:
    """A class that helps to get user input
    
    Args:
        var_name: name of var witch data is going to be stored
        print_data: data that is going to be printed
        isConverted: decides if the data should be converted to another type
        dtype: the type witch to be converted if isConverted turns out to be true
    """
    
    def __init__(self, var_name: str, print_data: str | None, isConverted: bool, dtype: Any):
        self.var_name = var_name
        self.print_data = print_data
        self.isConverted = isConverted
        self.dtype = dtype
        
    @c.boundscheck(False)  
    @c.wraparound(False)    
    def execute(self):
        if self.print_data != None:
            print(self.print_data, end="")
        value: str = input()
        
        data_obj: DataModule = local_memory[f'{self.var_name}REPLACE64@9']
        data_obj.value_change(value, self.isConverted)

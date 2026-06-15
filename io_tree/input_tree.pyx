from config.config import TokenType
from config.memory_config import set_memory
from modules.output_tree import Display
import logging
logger = logging.getLogger(' input')
logger.setLevel(logging.DEBUG)
from typing import Any
import cython as c

class Get:
    def __init__(self, numeric_list: list[int], token_list: list[Any], index: int):
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.index = index
        
    @c.boundscheck(False)  
    @c.wraparound(False)    
    def execute(self):
        var_name: str = self.token_list[self.index-2]
        var_name = var_name.replace(' ', '')
        if self.numeric_list[self.index+1] == TokenType.PARENTHESIS_OPEN.value and self.numeric_list[self.index+2] != TokenType.PARENTHESIS_CLOSE.value:
            display_obj: Display = Display(self.numeric_list, self.token_list, self.index)
            return_data: str
            _, return_data = display_obj.execute()
            print("DEBUG: input_tree: ",return_data, end=" ")
        value: str = input()
        set_memory(var_name, value)
        

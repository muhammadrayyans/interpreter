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
        self.__global_var_name: str
        self.__global_display: Display
        
    def validate(self) -> int:
        var_name: str = self.token_list[self.index-2]
        var_name = var_name.replace(' ', '')
        if self.numeric_list[self.index+1] == TokenType.PARENTHESIS_OPEN.value and self.numeric_list[self.index+2] != TokenType.PARENTHESIS_CLOSE.value:
            self.__global_display = Display(self.numeric_list, self.token_list, self.index)
        else:
            self.__global_display = None
        self.__global_var_name =   var_name
        
        return  0
    
    def execute(self):
        
        self.__global_display.execute()
        value: str = input()
        set_memory(self.__global_var_name, value)
        
        

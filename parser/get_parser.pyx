from config.config import TokenType, DataType
from modules.display_parser import ParserDisplay
import logging
from utils.utils import generate_index
logger = logging.getLogger(' parser_input')
logger.setLevel(logging.DEBUG)
from typing import Any
import cython as c
from array import array

class GetParser:
    """A class that helps to parse user input
    
    Args:
        numeric_list: list witch contains the numeric value of token elements
        token_list: the actual token list that gives the tokenized version of source code
        index: index of the current get call
    """
    
    def __init__(self, numeric_list: list[int], token_list: list[Any], index: int):
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.index = index
    
    
    @c.boundscheck(False)  
    @c.wraparound(False)  
    def execute(self)  -> tuple[str, Any, bool, Any, list]:
        var_name: str = self.token_list[self.index-2]
        return_data: str | None = None 
        jump_count: c.int = 1
        isConverted: bool = False
        skip_data: list = []
        var_name = var_name.replace(' ', '')
        
        if self.numeric_list[self.index+jump_count] != TokenType.PARENTHESIS_OPEN.value and int(self.numeric_list[self.index+jump_count]) in [DataType.INTEGER.value, DataType.FLOAT.value]:
            isConverted = True
            jump_count = 2
            
        if self.numeric_list[self.index+jump_count] == TokenType.PARENTHESIS_OPEN.value and self.numeric_list[self.index+jump_count+1] != TokenType.PARENTHESIS_CLOSE.value:
            display_obj: ParserDisplay = ParserDisplay(self.numeric_list, self.token_list, self.index)
            skip_data_display , return_data = display_obj.execute()
            skip_data = skip_data_display # increment 2 more needed i think --dev
        return var_name, return_data, isConverted, self.numeric_list[self.index+jump_count], skip_data
        
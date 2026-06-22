from config.config import TokenType, DataType, local_memory
from modules.display_parser import ParserDisplay
import logging
logger = logging.getLogger(' parser_input')
logger.setLevel(logging.DEBUG)
from typing import Any
import cython as c

class GetParser:
    """A class that helps to parse user input
    
    Args:
        numeric_list: list witch contains the numeric value of token elements
        token_list: the actual token list that gives the tokenized version of source code
        index: index of the current get call
    """
    
    def __init__(self, numeric_list: list[int], token_list: list[Any], index: int, scope=None):
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.index = index
        self.scope = scope
    
    
    @c.boundscheck(False)  
    @c.wraparound(False)  
    def execute(self)  -> tuple[str, Any, bool, Any]:
        var_name: str = self.token_list[self.index-2]
        return_data: str | None = None 
        jump_count: c.int = 2
        isConverted: bool = False
        var_name = var_name.replace(' ', '')
        
        if self.numeric_list[self.index+jump_count] != TokenType.PARENTHESIS_OPEN.value:
            if self.token_list[self.index+jump_count]  == DataType.INTEGER.name or self.token_list[self.index+jump_count]  == DataType.FLOAT.name:
                isConverted = True
                jump_count = 3
        else: pass
            
        if self.numeric_list[self.index+jump_count] == TokenType.PARENTHESIS_OPEN.value and self.numeric_list[self.index+jump_count+1] != TokenType.PARENTHESIS_CLOSE.value:
            display_obj: ParserDisplay = ParserDisplay(self.numeric_list, self.token_list, self.index+2)
            return_data = display_obj.execute()
        return var_name if self.scope == None or var_name in local_memory  else self.scope+var_name , return_data, isConverted, self.numeric_list[self.index+jump_count]
        
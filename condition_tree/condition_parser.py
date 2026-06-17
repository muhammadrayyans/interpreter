from config.config import TokenType
from typing import Any
import logging
logger = logging.getLogger(' condition_parser')
logger.setLevel(logging.DEBUG)

class ConditionParser:
    """A class tht gets both arguments and operation to be conducted
    
    Args:
        index: the index of the **assume** statement
    """
    
    def __init__(self, index: int, numeric_list: list, token_list: list[Any]) -> None:
        self.index = index
        self.numeric_list = numeric_list
        self.token_list = token_list
        
        
    def execute(self):
        loop_count: int = 1
        c_view: list = self.numeric_list
        evaluation_string: str = ''
        while c_view[self.index+loop_count] != TokenType.PARENTHESIS_CLOSE.value:
            # if self.token_list[self.index+loop_count][0] !=
            # if self.token_list[self.index+loop_count][0] != TokenType.QUOTE.name or self.token_list[self.index+loop_count][0] != TokenType.QUOTE.name:
                pass
    
    



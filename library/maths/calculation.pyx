from typing import Any
import config.config as config
from config.config import OperatorType, reverse_keyword, TokenType
from utils.utils import generate_index
from config.memory_config import get_memory
import cython as c
import logging 
logger = logging.getLogger(' calculation_lib')
logger.setLevel(logging.DEBUG)

class CalculationLib:
    """A class that helps to isolate numerical element and perform calculation
    
    Args:
        start_index: it gives the pointer from where the calculation should start in parsed code
        stop_char: it gives the end point to lookout for breaking the loop and giving the result
        token_list: the tokenized array of source code 
    """
    
    
    def __init__(self, start_index: int, stop_char: Any, token_list: list) -> None:
        self.start_index = start_index
        self.stop_char = stop_char
        self.token_list = token_list
    
    @c.boundscheck(False)
    @c.wraparound(False)
    def execute(self) -> tuple[list, Any]:
        # local variables
        global_skip: list = []
        loop_count: c.int = 0
        eval_string: str = ''
        isParenthesis: bool = False
        
        # main loop
        while self.start_index+loop_count < len(self.token_list) and self.token_list[self.start_index+loop_count] != self.stop_char:
            # setting i value
            i: Any = self.token_list[self.start_index+loop_count].replace(' ','')
            
            # checking whether i is a digit or not
            if i.isdigit():
                eval_string+=i
            
            # if i value is token type parenthesis open or close
            elif i == TokenType.PARENTHESIS_OPEN.name:
                eval_string+='('
                isParenthesis = not isParenthesis   
            elif i == TokenType.PARENTHESIS_CLOSE.name:
                if isParenthesis:
                    eval_string+=')'
                else:
                    eval_string+=''
                    
            # check if i value belongs to any operation
            elif i in [OperatorType.ADDITION.name, OperatorType.SUBTRACTION.name, OperatorType.MULTIPLICATION.name, OperatorType.DIVISION.name, OperatorType.MODULO.name]:
                try:
                    operator: str = reverse_keyword[OperatorType[i]]
                    eval_string+=operator
                except ValueError:
                    config.isError = True
            else:
                value: Any = get_memory(i)
                eval_string += str(value)
            
            loop_count+=1
            
        # removing last buffer ')' if there is one
        if eval_string[-1] == ')':
            eval_string=eval_string[:-1]

        # creating the skip list
        global_skip.extend(generate_index(self.start_index, self.start_index+loop_count))
        # evaluating the developed eval_string using eval()
        evaluation: Any = eval(eval_string)
        
        # returning the skip list and evaluation result
        return global_skip, evaluation
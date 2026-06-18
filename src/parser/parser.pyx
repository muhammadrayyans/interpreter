from config.config import TokenType, reverse_keyword
from colorama import init, Fore # type: ignore
import config.config as config
from typing import Any
import logging
import sys
# for suppressing python traceback
sys.tracebacklimit = 0 
import logging
import numpy as np # type: ignore
from utils.utils import generate_index
from modules.display_parser import ParserDisplay # type: ignore
from modules.output_tree import Display  # type: ignore
from modules.get_parser import GetParser # type: ignore
from modules.input_tree import Get # type: ignore
from array import array
from modules.variable_tree_config import VariableFormation # type: ignore
import cython as c
from condition_tree.condition_parser import ConditionParser
from condition_tree.condition_tree import Condition

logger = logging.getLogger(' parser')
logger.setLevel(logging.DEBUG)

class Parser:
    """A class that parses the Token data.

    Args:
        token_list: Tokenized list passed.
        numeric_token_list: Tokenized list converted to numeric passed.
    """
    
    def __init__(self, token_list: list[Any], numeric_list: list) -> None:
        self.token_list = token_list
        self.numeric_list = numeric_list
    
    def __condition_eval(self, inline_index: int, array_length: int, inline_new_line_count: int,  inline_target: TokenType) -> tuple[array, bool]:
        
        inline_skip_index: array = array('i',[])
        index = inline_index
        new_line_count = inline_new_line_count
        target: c.int = inline_target.value
        
        try:
            loop_count: c.int = 0
            isExists: bool = False
            
            while index+loop_count < array_length and self.numeric_list[index+loop_count] != TokenType.NEWLINE.value:
                if index+loop_count+1 < array_length and self.numeric_list[index+loop_count+1] == target:
                    isExists = True
                    break
                
                loop_count+=1
            
            if isExists != False:
                skip_count: c.int = 0
                if index+loop_count+2 < array_length:
                    skip_count=index+loop_count+2
                else:
                    skip_count=index+loop_count+1
                inline_skip_index.extend(generate_index(index, skip_count))
            
            if isExists == False:
                raise SyntaxError
            
        except SyntaxError:
                logging.error(Fore.RED+f" Syntax Missing at line {new_line_count+1} didn't closed the opening \033[4m\033[1m` {reverse_keyword.get(inline_target)} `\033[0m")
                config.isError = True
                return inline_skip_index, True
                
        return inline_skip_index, False                  
        
    @c.boundscheck(False)  
    @c.wraparound(False) 
    def execute(self):
        local_skip: array = array('i',[])
        local_isError: bool = False
        np_array = np.array(self.numeric_list, dtype=np.int32)
        c_view: c.int[:] = np_array # type: ignore 
        array_length: c.int = len(c_view) # type: ignore 
        index: c.int 
        new_line_count: c.int = 0
        
        for index in range(array_length):
            i = c_view[index] # type: ignore
            
            if local_isError:
                break
            
            if i == TokenType.NEWLINE.value:
                new_line_count+=1
                        
            elif np.isin(local_skip, index).any():
                continue
            
            elif i == TokenType.IF_CONDITION.value:
                condition_obj: ConditionParser = ConditionParser(index, self.numeric_list, self.token_list)
                exe_object = Condition(condition_obj)
                config.execute_thread.append(exe_object)
                
            
            elif i == TokenType.INPUT.value:
                get_object = GetParser(self.numeric_list, self.token_list, index) # type: ignore
                exe_obj = Get(get_object)
                config.execute_thread.append(exe_obj)
                
            elif i == TokenType.QUOTE:
                obj_skip, obj_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.QUOTE)
                local_skip.extend(obj_skip)
                local_isError = obj_isError
            
            elif i == TokenType.FORMAT:
                obj_skip, obj_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.FORMAT)
                local_skip.extend(obj_skip)
                local_isError = obj_isError

            elif i == TokenType.PARENTHESIS_OPEN.value:
                obj_skip, obj_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.PARENTHESIS_CLOSE)
                local_skip.extend(obj_skip)
                local_isError = obj_isError
                
            elif i == TokenType.BRACKETS_OPEN.value:
                obj_skip, obj_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.BRACKETS_CLOSE)
                local_skip.extend(obj_skip)
                local_isError = obj_isError
            
            elif i == TokenType.CURLY_BRACE_OPEN.value:
                obj_skip, obj_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.CURLY_BRACE_CLOSE)
                local_skip.extend(obj_skip)
                local_isError = obj_isError
            
            elif index+1 < len(c_view) and c_view[index+1] == TokenType.EQUAL.value : # type: ignore
                exe_obj = VariableFormation(self.token_list, self.numeric_list, index) # type: ignore
                config.execute_thread.append(exe_obj) 
                
            elif i == TokenType.PRINT.value:
                display_obj: ParserDisplay = ParserDisplay(self.numeric_list, self.token_list, index) # type: ignore
                exe_obj: Display = Display(display_obj)
                config.execute_thread.append(exe_obj)
                 

                
                
                
                
            

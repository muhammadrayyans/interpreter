from config.config import TokenType, reverse_keyword, config_skip_index
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
from modules.output_tree import Display
from array import array

logger = logging.getLogger(' parser')
logger.setLevel(logging.DEBUG)

class Parser:
    """A class that parses the Token data.

    Args:
        token_list: Tokenized list passed.
        numeric_token_list: Tokenized list converted to numeric passed.
    """
    def __init__(self, token_list: list[Any], numeric_list: list[int]) -> None:
        self.token_list = token_list
        self.numeric_list = numeric_list
    
    def __condition_eval(self, inline_index: int, array_length: int, inline_new_line_count: int,  inline_target: TokenType) -> tuple[list[int], bool]:
        
        inline_skip_index: list = []
        index = inline_index
        new_line_count = inline_new_line_count
        target: int = inline_target.value
        
        try:
            loop_count: int = 0
            isExists: bool = False
            
            while index+loop_count < array_length and self.numeric_list[index+loop_count] != TokenType.NEWLINE.value:
                if index+loop_count+1 < array_length and self.numeric_list[index+loop_count+1] == target:
                    isExists = True
                    break
                
                loop_count+=1
            
            if isExists != False:
                skip_count: int = 0
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
                return [], True
                
        return inline_skip_index, False                  
        
    
    def execute(self):
        local_skip: array = array('i',[])
        local_isError: bool = False
        np_array = np.array(self.numeric_list, dtype=np.int32)
        # c_view: c.int[:] = np_array
        array_length: int = len(self.numeric_list)
        index: int 
        new_line_count: int = 0
        
        for index in range(array_length):
            i = self.numeric_list[index]
            
            if local_isError:
                break
            
            if i == TokenType.NEWLINE.value:
                new_line_count+=1
                
            elif np.isin(local_skip, index).any():
                continue
            
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
            
            elif i == TokenType.PRINT.value:
                display_obj: ParserDisplay = ParserDisplay(self.numeric_list, self.token_list, index)
                obj_skip_index, print_data = display_obj.evaluate()
                exe_obj: Display = Display(print_data)
                local_skip.extend(obj_skip_index)
                config.execute_thread.append(exe_obj)
                
                
                
            

import logging
import config.config as config
from config.config import TokenType, reverse_keyword
from typing import Any
from colorama import init, Fore # type: ignore
import sys
# for suppressing python traceback
sys.tracebacklimit = 0 
import logging
import numpy as np # type: ignore
from utils.utils import generate_index

logger = logging.getLogger(' parser')
logger.setLevel(logging.DEBUG)

class Parser:
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
        local_skip: list = []
        local_isError: bool = False
        array_length: int = len(self.numeric_list)
        index: int 
        new_line_count: int = 0
        
        for index in range(array_length):
            
            i = self.numeric_list[index]
            
            if np.isin(local_skip, index).any():
                continue
                
            elif local_isError:
                break
            
            elif i == TokenType.NEWLINE.value:
                new_line_count+=1
                continue
            
            elif i == TokenType.PARENTHESIS_OPEN.value:
                function_skip_index, local_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.PARENTHESIS_CLOSE)
                local_skip.extend(function_skip_index)
                continue
                       
            elif i == TokenType.QUOTE.value:
                function_skip_index, local_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.QUOTE)
                local_skip.extend(function_skip_index)
                continue
                
            elif i == TokenType.FORMAT.value:
                function_skip_index, local_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.FORMAT)
                local_skip.extend(function_skip_index)
                continue
                
            elif i == TokenType.CURLY_BRACE_OPEN.value:
                function_skip_index, local_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.CURLY_BRACE_CLOSE)
                local_skip.extend(function_skip_index)
                continue
                
            elif i == TokenType.BRACKETS_OPEN.value:
                function_skip_index, local_isError = self.__condition_eval(index, array_length, new_line_count, TokenType.BRACKETS_CLOSE)
                local_skip.extend(function_skip_index)
                continue
                
            elif index+1 < array_length and i == TokenType.EQUAL.value:
                target: int = self.numeric_list[index+1]
                try:
                    if target == 0:
                        raise ValueError
                    loop_count: int = 2
                    isExists: bool = False
                    while index+loop_count+1 < array_length and self.numeric_list[index+loop_count] != TokenType.NEWLINE.value:
                        if index+loop_count+1 < array_length and self.numeric_list[index+loop_count+1] == target:
                            isExists = True
                        loop_count+=1
                        
                    if not isExists:
                        raise SyntaxError
                    else :
                        continue
                    
                except SyntaxError:
                        logging.error(Fore.RED+f" Syntax Missing at line {new_line_count+1} didn't closed the opening \033[4m\033[1m` {reverse_keyword.get(TokenType(target))} `\033[0m")
                        config.isError = True
                        break
                    
                except  ValueError:
                        logging.error(Fore.RED+f" Syntax Missing at line {new_line_count+1} use ', `,"+' or ",'+f" before \033[4m\033[1m'{self.token_list[index+1]}'\033[0m to add a value")
                        config.isError = True
                        break
            

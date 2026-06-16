from config.config import TokenType, reverse_keyword, OperatorType
from config.memory_config import get_memory, set_memory
import config.config as config
from utils.utils import generate_index
import numpy as np # type: ignore
import logging
import cython as c
logger = logging.getLogger(' var_tree')
logger.setLevel(logging.DEBUG)
from typing import Any
from array import array
from colorama import init,  Fore # type: ignore 

# var node replace every var in token code
class VariableFormation:
    """A class that assign value to variables
    Args:
        token_list: Tokenized list passed.
        numeric_token_list: Tokenized list converted to numeric passed.
    """
    
    # constructor of class
    def __init__(self, token_list: list[Any], numeric_list: list[int]):
        self.token_list = token_list 
        self.numeric_list = numeric_list
        
    # execute code
    @c.boundscheck(False)  
    @c.wraparound(False)   
    def execute(self):
        
        # main skip list for optimization
        def_skip: array = array('i',[])
        index: c.int
        i: c.int
        np_array = np.array(self.numeric_list, dtype=np.int32)
        c_view: c.int[:] = np_array # type: ignore 
        limit: c.int = len(c_view) # type: ignore 
        
        # for loop for var adding
        for index in range(limit):
            i = c_view[index] # type: ignore 
            
            # skip if value exist in skip list
            if index != 0 and np.isin(def_skip, index).any():
                continue
            
            # skip for numeric
            elif index+1 < limit and i == 0 and c_view[index+1] == TokenType.EQUAL.value and reverse_keyword.get(self.token_list[index+2]) != None: #type: ignore
                continue
            
            # check if its a var by checking if bef is = and after it have some value 
            elif index+1 < limit and i == 0 and c_view[index+1] == TokenType.EQUAL.value: #type: ignore
                
                
                var_name: str = self.token_list[index]
                variable_value: str = ''
                loop_count: c.int = 0
                skip_index: array = array('i',[])
                
                # loops from = until it reach a newline or list index out of range
                while loop_count+index < limit and c_view[loop_count+index] != TokenType.NEWLINE.value and c_view[loop_count+index] != TokenType.PARENTHESIS_CLOSE.value : #type: ignore
                    
                    # skip index check for optimized code
                    if index+loop_count != 0 and np.isin(skip_index, index+loop_count).any():
                        loop_count+=1
                        continue
                    
                    # numbers
                    if self.token_list[loop_count+index+1] == TokenType.EQUAL.name and self.token_list[loop_count+index+2] not in ['QUOTE', 'FORMAT']: # type: ignore
                        var_name: str = self.token_list[loop_count+index].replace(' ','')
                        if self.token_list[loop_count+index+2] == TokenType.PARENTHESIS_OPEN.name or  not isinstance(self.token_list[loop_count+index+2], TokenType):
                            inline_loop_count: c.int = 2
                            evaluation_string: str = ''
                            
                            
                            try:    
                                
                                if self.token_list[loop_count+index+inline_loop_count] != TokenType.NEWLINE.name:
                                    while inline_loop_count < limit and self.token_list[loop_count+index+inline_loop_count] != TokenType.NEWLINE.name:
                                        
                                        # checks if the next element is a number
                                        if self.token_list[loop_count+index+inline_loop_count].replace(' ','').isdigit():
                                            evaluation_string+=self.token_list[loop_count+index+inline_loop_count]
                                            if self.token_list[loop_count+index+inline_loop_count+1] != TokenType.NEWLINE.name:
                                                if self.token_list[loop_count+index+inline_loop_count+1] == TokenType.PARENTHESIS_CLOSE.name:
                                                    evaluation_string+=')'
                                                else: 
                                                    if self.token_list[loop_count+index+inline_loop_count] != TokenType.NEWLINE.name:
                                                        evaluation_string+=str(reverse_keyword[OperatorType[self.token_list[loop_count+index+inline_loop_count+1]]])
                                                    else: break
                                                inline_loop_count+=2
                                            else: break
                                                                                  
                                        # checks if the current one is a parenthesis
                                        elif self.token_list[loop_count+index+inline_loop_count] == TokenType.PARENTHESIS_OPEN.name:
                                            evaluation_string+='('
                                            inline_loop_count+=1
                                            if self.token_list[loop_count+index+inline_loop_count+1] == TokenType.NEWLINE.name or isinstance(self.token_list[loop_count+index+inline_loop_count+1], TokenType):
                                                raise SyntaxError
                                        
                                        # checking for var
                                        else: 
                                            call_var: str = self.token_list[loop_count+index+inline_loop_count].replace(' ','')
                                            numeric_value: str = str(get_memory(call_var))
                                            evaluation_string += numeric_value
                                            if self.token_list[loop_count+index+inline_loop_count+1] != TokenType.NEWLINE.name:
                                                if self.token_list[loop_count+index+inline_loop_count+1] == TokenType.PARENTHESIS_CLOSE.name:
                                                    evaluation_string+=')'
                                                else: 
                                                    if self.token_list[loop_count+index+inline_loop_count] != TokenType.NEWLINE.name:
                                                        evaluation_string+=str(reverse_keyword[OperatorType[self.token_list[loop_count+index+inline_loop_count+1]]])
                                                    else: break
                                                inline_loop_count+=2
                                            else: break
                                        
                                
                            except SyntaxError:
                                logging.error(Fore.RED+f" Syntax mistake with declaring numerical value at '\033[4m\033[1m{var_name}\033[0m")
                                config.isError = True
                                break
                            
                            result = eval(evaluation_string)
                            set_memory(var_name, result)
                            skip_index.extend(generate_index(index+loop_count, index+loop_count+inline_loop_count+1))
                            
                            loop_count+=1
                            continue
                    
                    # string        
                    else:   
                        # normal var to var match case
                        if loop_count+index+2 < len(self.numeric_list) and c_view[loop_count+index+2] == 0 and c_view[loop_count+index+1] == TokenType.EQUAL.value: #type: ignore
                            self.token_list[loop_count+index+2] = self.token_list[loop_count+index+2].replace(' ','')
                            value_normal: str | c.int | None = get_memory(self.token_list[loop_count+index+2])
                            variable_value+=str(value_normal)
                            skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
                        
                        # formatted string match case
                        elif c_view[loop_count+index] == TokenType.CURLY_BRACE_OPEN.value: #type: ignore
                            result: str | c.int | None = get_memory(self.token_list[loop_count+index+1]) if loop_count+index < len(self.numeric_list) else None
                            if result != None:
                                value: c.int = loop_count+index+1
                                variable_value+='{'
                                variable_value+=f'{self.token_list[value]}'
                                variable_value+='}'
                                loop_count+=1
                                skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
                            
                        # normal string match case
                        elif index+loop_count > 0 and c_view[index+loop_count-1] == TokenType.QUOTE.value and i == 0: #type: ignore
                            variable_value+='~'
                            variable_value += self.token_list[index+loop_count]
                        
                        # formatted string normal text add case
                        elif index >= 0 and c_view[index+loop_count-1] == TokenType.FORMAT.value and i == 0: # type: ignore
                            variable_value += self.token_list[index+loop_count]
                        
                        # formatted string after var text add case
                        elif index > 0 and c_view[index+loop_count-1] == TokenType.CURLY_BRACE_CLOSE.value and i == 0: #type: ignore
                            if c_view[index+loop_count] == 0: #type: ignore
                                variable_value += self.token_list[index+loop_count]
                        
                        # formatting var name to remove un necessary space 
                        var_name = var_name.replace(' ','')
                        set_memory(var_name, variable_value)
                        
                        # incrementing loop
                        loop_count+=1
                    
                    # adding current skip index to for loop skip index too
                    def_skip.extend(skip_index)
                    
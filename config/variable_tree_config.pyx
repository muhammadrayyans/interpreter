from config.config import TokenType, reverse_keyword
from utils.utils import generate_index
from config.memory_config import get_memory, set_memory
import numpy as np # type: ignore
import logging
import cython as c
logger = logging.getLogger(' var_tree')
logger.setLevel(logging.DEBUG)
from typing import Any

# var node replace every var in token code
class VariableFormation:
    
    # constructor of class
    def __init__(self, token_list: list[Any], numeric_list: list[int]):
        self.token_list = token_list # dev
        self.numeric_list = numeric_list
        
    # execute code
    def execute(self):
        
        # main skip list for optimization
        def_skip: list = []
        index: c.int
        i: c.int
        limit: c.int = len(self.numeric_list)
        
        # for loop for var adding
        for index in range(limit):
            i = self.numeric_list[index]
            # skip if value exist in skip list
            if index != 0 and np.isin(def_skip, index).any():
                continue
            
            elif index+1 < len(self.numeric_list) and i == 0 and self.numeric_list[index+1] == TokenType.EQUAL.value and reverse_keyword.get(self.token_list[index+2]) != None:
                continue
            
            # check if its a var by checking if bef is = and after it have some value 
            elif index+1 < len(self.numeric_list) and i == 0 and self.numeric_list[index+1] == TokenType.EQUAL.value:
                
                
                var_name: str = self.token_list[index]
                variable_value: str = ''
                loop_count: c.int = 0
                skip_index: list = []
                
                # loops from = until it reach a newline or list index out of range
                while loop_count+index < len(self.numeric_list) and self.numeric_list[loop_count+index] != TokenType.NEWLINE.value and self.numeric_list[loop_count+index] != TokenType.PARENTHESIS_CLOSE.value :
                    
                    # skip index check for optimized code
                    if index+loop_count != 0 and np.isin(skip_index, index+loop_count).any():
                        loop_count+=1
                        continue
                    
                    # normal var to var match case
                    elif loop_count+index+2 < len(self.numeric_list) and self.numeric_list[loop_count+index+2] == 0 and self.numeric_list[loop_count+index+1] == TokenType.EQUAL.value:
                        self.token_list[loop_count+index+2] = self.token_list[loop_count+index+2].replace(' ','')
                        value_normal: str | c.int | None = get_memory(self.token_list[loop_count+index+2])
                        variable_value+=str(value_normal)
                        skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
                    
                    # formatted string match case
                    elif self.numeric_list[loop_count+index] == TokenType.CURLY_BRACE_OPEN.value:
                        result: str | c.int | None = get_memory(self.token_list[loop_count+index+1]) if loop_count+index < len(self.numeric_list) else None
                        if result != None:
                            value: c.int = loop_count+index+1
                            variable_value+='{'
                            variable_value+=f'{self.token_list[value]}'
                            variable_value+='}'
                            loop_count+=1
                            skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
                            continue
                    
                    # normal string match case
                    elif index+loop_count > 0 and self.numeric_list[index+loop_count-1] == TokenType.QUOTE.value and i == 0:
                        variable_value+='~'
                        variable_value += self.token_list[index+loop_count]
                    
                    # formatted string normal text add case
                    elif index > 0 and self.token_list[index+loop_count-1] == TokenType.FORMAT.name and i == 0:
                        variable_value += self.token_list[index+loop_count]
                    
                    # formatted string after var text add case
                    elif index > 0 and self.numeric_list[index+loop_count-1] == TokenType.CURLY_BRACE_CLOSE.value and i == 0:
                        if self.numeric_list[index+loop_count] == 0:
                            variable_value += self.token_list[index+loop_count]
                       
                    # formatting var name to remove un necessary space 
                    var_name = var_name.replace(' ','')
                    set_memory(var_name, variable_value)
                    
                    # incrementing loop
                    loop_count+=1
                
                # adding current skip index to for loop skip index too
                def_skip.extend(skip_index)
                
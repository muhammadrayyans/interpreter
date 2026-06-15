from config.config import TokenType, reverse_keyword, local_memory
from utils.utils import  generate_index
import numpy as np # type: ignore
from config.memory_config import get_memory
import logging
logger = logging.getLogger(' display_parser')
logger.setLevel(logging.DEBUG)
import cython as c
from typing import Any
from array import array

class ParserDisplay:
    """A class that parses the display data.

    Args:
        index: Display keyword index.
        token_list: Tokenized list passed.
        numeric_token_list: Tokenized list converted to numeric passed.
    """
    
    # constructor for print function
    def __init__(self, numeric_list: list[int], token_list: list, index: int):
        self.index = index+2
        self.token_list = token_list
        self.numeric_list = numeric_list
        
    # execute method
    @c.boundscheck(False)  
    @c.wraparound(False)
    def evaluate(self) -> tuple[array, str]:
        global_skip: array = array('i', [])
        skip_def: array = array('i', [])
        limit: c.int = len(self.numeric_list[self.index : ])
        np_array = np.array(self.numeric_list, dtype=np.int32)
        c_view: c.int[:] = np_array # type: ignore 
        numeric_list_len: c.int = len(c_view) # type: ignore 
        print_string: str = ''
        key: c.int
        i: c.int

        # main loop runs from index 
        for key in range(limit):
            i = c_view[key+self.index] # type: ignore 
            
            if np.isin(skip_def, self.index+key).any():
                continue
            
            # condition to make sure its not out of scope
            elif i != TokenType.PARENTHESIS_CLOSE.value:
                
                # if i param found to be formatted type execute formatted code
                if i == TokenType.FORMAT.value:
                    loop_count: c.int = 0
                    skip_index: list = []
                    string_var: str = '' # type: ignore
                    while self.index+key+loop_count+1 < numeric_list_len and c_view[self.index+key+loop_count+1] != TokenType.FORMAT.value: # type: ignore
                        
                        if np.isin(skip_index, self.index+key+loop_count).any():
                            string_var+=' ' # type: ignore
                            loop_count+=1
                            continue
                        
                        # core of formatted code replace '{' with actual value if found else raise key error
                        elif c_view[self.index+key+loop_count] == TokenType.CURLY_BRACE_OPEN.value: # type: ignore
                            result_data: str | None = get_memory(self.token_list[self.index+key+loop_count+1])
                            if result_data != None:
                                string_var+=result_data.format(**local_memory)
                                skip_index.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count+2))
                                loop_count+=1
                                continue

                        else: 
                            if c_view[self.index+key+loop_count] == 0: # type: ignore
                                string_var+=self.token_list[self.index+key+loop_count]    
                            elif c_view[self.index+key+loop_count] == TokenType.CURLY_BRACE_CLOSE.value and c_view[self.index+key+loop_count+1] == 0: # type: ignore
                                string_var+=self.token_list[self.index+key+loop_count+1]
                            loop_count+=1
                    
                    # adding the received data to print data
                    print_string+=str(string_var)
                    skip_def.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count))   
                    break 
                
                # if param is double quote print as it is
                elif i == TokenType.QUOTE.value:
                    loop_count: c.int = 1
                    skip_index: list = []
                    string_var: str = '' # type: ignore
                    while self.index+key+loop_count+1 < numeric_list_len and c_view[self.index+key+loop_count] != TokenType.QUOTE.value and c_view[self.index+key+loop_count] != TokenType.NEWLINE.value: # type: ignore
                        try:
                            value: TokenType = TokenType(c_view[self.index+key+loop_count]) # type: ignore
                            
                            if value != None and c_view[self.index+key+loop_count] != TokenType.QUOTE.value: # type: ignore
                                string_var += str(reverse_keyword.get(value)) # type: ignore                     

                        except ValueError:
                            
                            if c_view[self.index+key+loop_count] != TokenType.QUOTE.value and c_view[self.index+key+loop_count] != TokenType.NEWLINE.value: # type: ignore
                                string_var+= self.token_list[self.index+key+loop_count]
                                
                        loop_count+=1
                        
                    print_string+=str(string_var)
                    skip_def.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count))
                    break
                
                # if its direct var printing prints it wih char getting, separated by comma multiple var can be specified
                elif i == 0 and c_view[self.index+key-1] == TokenType.PARENTHESIS_OPEN.value: # type: ignore
                    loop_count:  c.int = 0
                    while self.index+key+loop_count < numeric_list_len and c_view[self.index+key+loop_count] != TokenType.PARENTHESIS_CLOSE.value and c_view[self.index+key+loop_count] != TokenType.NEWLINE.value: # type: ignore
                        if c_view[self.index+key+loop_count] == 0: # type: ignore
                            self.token_list[self.index+key+loop_count] = self.token_list[self.index+key+loop_count].replace(' ','')
                            if get_memory(self.token_list[self.index+key+loop_count]) != None:
                                string_var: str | None = get_memory(self.token_list[self.index+key+loop_count])  
                                print_string+=str(string_var)
                            else:
                                raise KeyError
                        else:
                            print_string+=' '
                        loop_count+=1
                    skip_def.extend(generate_index(self.index+key, self.index+key+loop_count))
                    break
                    
        global_skip.extend(skip_def)
        return global_skip, print_string
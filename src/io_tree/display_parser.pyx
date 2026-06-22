from config.config import TokenType, reverse_keyword, local_memory
from utils.utils import  generate_index
import numpy as np # type: ignore
from config.memory_config import get_memory
import logging
logger = logging.getLogger(' display_parser')
logger.setLevel(logging.DEBUG)
import cython as c

class ParserDisplay:
    """A class that parses the display data.

    Args:
        index: Display keyword index.
        token_list: Tokenized list passed.
        numeric_token_list: Tokenized list converted to numeric passed.
    """
    
    # constructor for print function
    def __init__(self, numeric_list: list[int], token_list: list, index: int, scope=None):
        self.index = index+2
        self.token_list = token_list
        self.numeric_list = numeric_list
        self.skip_value: list = []
        self.scope = scope
        
    # execute method
    @c.boundscheck(False)  
    @c.wraparound(False)
    
    def execute(self) ->  str:
        skip_def: list = []
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
                            if self.token_list[self.index+key+loop_count+1] in local_memory:
                                self.scope=None
                            result_data: str = str(get_memory(self.token_list[self.index+key+loop_count+1] , self.scope))
                            if result_data != None:
                                string_var+= result_data # type: ignore
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
                    skip_def.extend(generate_index(self.index, self.index+key+loop_count))   
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
                    skip_def.extend(generate_index(self.index+key, self.index+key+loop_count))
                    break
                
                # if its direct var printing prints it wih char getting, separated by comma multiple var can be specified
                elif i == 0 and c_view[self.index+key-1] == TokenType.PARENTHESIS_OPEN.value: # type: ignore
                    loop_count:  c.int = 0
                    while self.index+key+loop_count < numeric_list_len and c_view[self.index+key+loop_count] != TokenType.PARENTHESIS_CLOSE.value and c_view[self.index+key+loop_count] != TokenType.NEWLINE.value: # type: ignore
                        if c_view[self.index+key+loop_count] == 0: # type: ignore
                            self.token_list[self.index+key+loop_count] = self.token_list[self.index+key+loop_count].replace(' ','')
                            if self.token_list[self.index+key+loop_count+1] in local_memory:
                                self.scope=None
                            if get_memory(self.token_list[self.index+key+loop_count], self.scope) != None:
                                string_var: str | None = str(get_memory(self.token_list[self.index+key+loop_count], self.scope))
                                print_string+=string_var
                            else:
                                raise KeyError
                        else:
                            print_string+=' '
                        loop_count+=1
                    skip_def.extend(generate_index(self.index+key, self.index+key+loop_count))
                    break
                    
        self.skip_value.extend(skip_def)
        return print_string
    

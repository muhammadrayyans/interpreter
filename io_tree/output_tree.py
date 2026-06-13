from config.config import TokenType, reverse_keyword
from utils.utils import  generate_index
import numpy as np # type: ignore
from config.memory_config import get_memory
import logging
logger = logging.getLogger(' output_tree')
logger.setLevel(logging.DEBUG)

class Display:
    
    # constructor for print function
    def __init__(self, list: list[int], token_list: list[any], index: int):
        self.index = index+2
        self.token_list = token_list
        self.numeric_list = list
        
    # execute method
    def execute(self) -> tuple[str, list[int]]:
        global_skip = []
        skip_def = []
        numeric_list_len = len(self.numeric_list)
        print_string = ''

        # main loop runs from index 
        for key, i in enumerate(self.numeric_list[self.index : ]):
            if np.isin(skip_def, self.index+key).any():
                continue
            
            # condition to make sure its not out of scope
            elif i != TokenType.PARENTHESIS_CLOSE.value:
                
                # if i param found to be formatted type execute formatted code
                if i == TokenType.FORMAT.value:
                    loop_count = 0
                    skip_index = []
                    string_var = f''
                    while self.index+key+loop_count+1 < numeric_list_len and self.numeric_list[self.index+key+loop_count+1] != TokenType.FORMAT.value:
                        
                        if np.isin(skip_index, self.index+key+loop_count).any():
                            string_var+=' '
                            loop_count+=1
                            continue
                        
                        # core of formatted code replace '{' with actual value if found else raise key error
                        elif self.numeric_list[self.index+key+loop_count] == TokenType.CURLY_BRACE_OPEN.value:
                            result = get_memory(self.token_list[self.index+key+loop_count+1])
                            if result != None:
                                string_var+=result
                                skip_index.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count+2))
                                loop_count+=1
                                continue
                            else:
                                raise KeyError
                        else: 
                            if self.numeric_list[self.index+key+loop_count] == 0:
                                string_var+=self.token_list[self.index+key+loop_count]    
                            elif self.numeric_list[self.index+key+loop_count] == TokenType.CURLY_BRACE_CLOSE.value and self.numeric_list[self.index+key+loop_count+1] == 0:
                                string_var+=self.token_list[self.index+key+loop_count+1]
                            loop_count+=1
                    
                    # adding the received data to print data
                    print_string+=string_var
                    skip_def.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count))   
                    break 
                
                # if param is double quote print as it is
                elif i == TokenType.QUOTE.value:
                    loop_count = 0
                    skip_index = []
                    string_var = ''
                    while self.index+key+loop_count+1 < numeric_list_len and self.numeric_list[self.index+key+loop_count+1] != TokenType.QUOTE.value:
                        try:
                            value = reverse_keyword.get(TokenType(self.numeric_list[self.index+key+loop_count]))
                            if value != None and self.numeric_list[self.index+key+loop_count] != TokenType.QUOTE.value :
                                string_var+=value
                        except ValueError:
                            string_var+= self.token_list[self.index+key+loop_count]
                        loop_count+=1
                    print_string+=string_var
                    skip_def.extend(generate_index(self.index+key+loop_count, self.index+key+loop_count))
                    break
                    
                # if its direct var printing prints it wih char getting, separated by comma multiple var can be specified
                elif i == 0 and self.numeric_list[self.index+key-1] == TokenType.PARENTHESIS_OPEN.value:
                    loop_count=0
                    while self.index+key+loop_count < numeric_list_len and self.numeric_list[self.index+key+loop_count] != TokenType.PARENTHESIS_CLOSE:
                        if self.numeric_list[self.index+key+loop_count] == 0:
                            self.token_list[self.index+key+loop_count] = self.token_list[self.index+key+loop_count].replace(' ','')
                            if get_memory(self.token_list[self.index+key+loop_count]) != None:
                                string_var = get_memory(self.token_list[self.index+key+loop_count])  
                                print_string+=string_var
                            else:
                                raise KeyError
                        else:
                            print_string+=f' '
                        loop_count+=1
                    skip_def.extend(generate_index(self.index+key, self.index+key+loop_count))
        global_skip.extend(skip_def)
        
        logger.debug(print_string)
        return skip_def
                
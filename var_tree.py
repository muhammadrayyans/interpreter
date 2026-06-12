from config import TokenType
from utils import debug, generate_index
from memory_function import get_memory, set_memory
import numpy as np # type: ignore

# var node replace every var in token code
class VariableFormation:
    def __init__(self, token_list: list[any], numeric_list: list[int]):
        self.token_list = token_list # dev
        self.numeric_list = numeric_list
        
    # execute code
    def execute(self):
        # main skip list for optimization
        def_skip = []
        
        # for loop for var adding
        for index, i in enumerate(self.numeric_list):
            # skip if value exist in skip list
            if np.isin(def_skip, index).any():
                loop_count+=1
                continue
               
            # check if its a var by checking
            elif index+1 < len(self.numeric_list) and i == 0 and self.numeric_list[index+1] == TokenType.EQUAL.value:
                var_name = self.token_list[index]
                variable_value = ''
                loop_count = 0
                skip_index = []
                while loop_count+index < len(self.numeric_list) and self.numeric_list[loop_count+index] != TokenType.NEWLINE.value :
                    if np.isin(skip_index, index+loop_count).any():
                        loop_count+=1
                        continue
                    
                    elif self.numeric_list[loop_count+index] == TokenType.CURLY_BRACE_OPEN.value:
                        result = get_memory(self.token_list[loop_count+index+1]) if loop_count+index < len(self.numeric_list) else None
                        if result != None:
                            variable_value+=result   
                            loop_count+=1
                            skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
                            continue
                        
                    elif self.numeric_list[index+loop_count-1] == TokenType.QUOTE.value and i == 0:
                        variable_value += self.token_list[index+loop_count]
                    
                    elif index > 0 and self.token_list[index+loop_count-1] == TokenType.FORMAT.name and i == 0:
                        variable_value += self.token_list[index+loop_count]
                        
                    elif index > 0 and self.numeric_list[index+loop_count-1] == TokenType.CURLY_BRACE_CLOSE.value and i == 0:
                        if self.numeric_list[index+loop_count] == 0:
                            variable_value += self.token_list[index+loop_count]
                        
                    var_name = var_name.replace(' ','')
                    set_memory(var_name, variable_value)
                    
                    loop_count+=1
                    
                def_skip.extend(skip_index)
                
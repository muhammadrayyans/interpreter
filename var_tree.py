from config import TokenType
from utils import debug, generate_index
from memory_function import get_memory, set_memory
import numpy as np # type: ignore

class VariableFormation:
    def __init__(self, token_list: list[any], numeric_list: list[int]):
        self.token_list = token_list # dev
        self.numeric_list = numeric_list
    def execute(self):
        for index, i in enumerate(self.numeric_list):
            debug("i val", i)
            if index+1 < len(self.numeric_list) and i == 0 and self.numeric_list[index+1] == TokenType.EQUAL.value:
                
                variable_value = ''
                loop_count = 0
                skip_index = []
                while loop_count+index < len(self.numeric_list) and self.numeric_list[loop_count+index] != TokenType.FORMAT.value and self.numeric_list[loop_count+index] != TokenType.NEWLINE.value:
                    if np.isin(skip_index, index+loop_count).any():
                        loop_count+=1
                        continue
                    
                    if self.numeric_list[loop_count+index] == TokenType.CURLY_BRACE_OPEN:
                        debug("reach", "")
                        result = get_memory(self.token_list.get([loop_count+index])) if loop_count+index < len(self.numeric_list) else None
                        variable_value+=result if result != None else None
                        skip_index.extend(generate_index(index+loop_count, index+loop_count+2))
             
                    elif not isinstance(i, int):
                        variable_value += i
                    loop_count+=1
                debug("var", variable_value)
                
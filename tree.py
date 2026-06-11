from memory_function import get_memory
from utils import debug, generate_index
from config import keyword, TokenType
import numpy as np # type: ignore

# class for var tree
class VariableTree:
    global_skip = []
    
    def __init__(self, token_list : list, content_index: int):
        self.token_list = token_list
        self.content = content_index
          
    def string(self) -> tuple[str, list]:
        loop_count = 0
        return_string = ''
        while  self.content+loop_count < len(self.token_list) and self.content+loop_count != '"' and self.token_list[self.content+loop_count] != '\n':
            return_string+=str(self.token_list[self.content+loop_count]) if self.content+loop_count < len(self.token_list) else None
            loop_count+=1
        
        self.global_skip.extend(generate_index(self.content, self.content+loop_count))
        return return_string,self.global_skip
    
    def formatted_string(self):
        debug("", self.token_list)
        loop_count = 0
        return_string = ''
        skip_index = []
        while self.content+loop_count+1 < len(self.token_list) and self.token_list[self.content+loop_count] != "`"  and self.token_list[self.content+loop_count] != TokenType.PARENTHESIS_CLOSE.value and self.token_list[self.content+loop_count] != TokenType.NEWLINE.value and self.token_list[self.content+loop_count] != TokenType.FORMAT.value:    
            if np.isin(skip_index, self.content+loop_count).any():
                loop_count+=1
                continue
                
            elif self.token_list[self.content+loop_count] == '{' or self.token_list[self.content+loop_count] == TokenType.CURLY_BRACE_OPEN.value:
                var_value = get_memory(self.token_list[self.content+loop_count+1])
                return_string+=str(var_value)
                skip_index.extend(generate_index((self.content+loop_count), (self.content+loop_count+3)))
                loop_count+=1
                continue

            else:
                if self.content+loop_count < len(self.token_list) and isinstance((self.token_list[self.content+loop_count]) , str):
                    return_string+=(self.token_list[self.content+loop_count]) 
                loop_count+=1
            self.global_skip.extend(generate_index(self.content, self.content+loop_count+1))
        return return_string, self.global_skip
        

    

    
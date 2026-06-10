from utils import debug, generate_index
import numpy as np # type: ignore
from memory_function import get_memory # dev --debug
from tree import VariableTree
from config import TokenType, keyword

TokenType = TokenType
keyword = keyword

# tokenization function 
class Tokenization:
    
    # constructor of a basic token. work using token passed
    def __init__(self, token_value : str):
        self.token = keyword[token_value]
        self.value = self.token.value
        
    # returns the token value witch the keyword passed
    def token_value(self) -> int:
        return self.value


# token list builder function accepting the source code
def tokenize_var(list: list) -> list:
    
    # creating temporary space for storing value
    token_list = []
    # skip index for skipping un necessary loops
    skip_index = []
    # calling the token abstract tree as class obj
    token_converter = Tokenization
    #looping through the list witch was formatted
    for index, x in enumerate(list):
        # formatting the loop with filters
        list = [x for x in list if x not in [' ', '']]
        
        # skipping if skip index exist or the sting is completely empty
        if np.isin(skip_index, index).any() or x == '' or x == " ":
            # adding the elements to the token even if skipped
            continue
        
        # using try catch block for safety and catching errors
        try:
            # checking if token value exist for provided keyword if none raise error
            if keyword.get(x) != None:
                match token_converter.token_value(keyword.get(x)):
                    # else get the corresponding data to temp storage
                    case _:
                        token_list.append(token_converter.token_value(keyword[x]))
            else : raise KeyError  
        # excepting the key error and using the variable itself as the token witch is essential for variable declaration
        except KeyError:
            if index+1 < len(list) and keyword[list[index+1]] == TokenType.EQUAL and keyword.get(index+1) == None:
                variable_obj = VariableTree(list, index+1)
                result, skip_list = variable_obj.set_variable()
                token_list.append(result)
                skip_index.extend(skip_list)
                
            # added normal strings
            token_list.append(x)
            
    # returning the tokenized list
    return token_list

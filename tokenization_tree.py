from utils import debug, generate_index
import numpy as np # type: ignore
from memory_function import set_memory
from tree import VariableTree
from config import TokenType, keyword, config_skip_index

TokenType = TokenType
keyword = keyword

# tokenization function 
class Tokenization:
    
    # constructor of a basic token. work using token passed
    def __init__(self, token_value : str):
        self.token = keyword[token_value]
        self.value = self.token.value
        
    # returns the token value witch the keyword passed
    def token_value(self):
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
    # formatting the loop with filters
    list = [x for x in list if x not in [' ', '']]
    list = ['`' if x == "'" else x for x in list]
    for index, x in enumerate(list):
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
                        token_list.append(keyword[x].name)
            else : raise KeyError  
        # excepting the key error and using the variable itself as the token witch is essential for variable declaration
        except KeyError:
            token_list.append(x)
            
    # returning the tokenized list
    return token_list

# numeric list for better performance
def numeric_var(list: list) -> list[int]:
    numeric_list = []
    for i in list:
        # checking if i has corresponding value in keywords
        try:
            if TokenType[i]:
                # adding the value of the corresponding enum
                numeric_list.append(TokenType[i].value)
        except KeyError:
            # as a placeholder adds 0
            numeric_list.append(0)
    # returning the new list
    return numeric_list
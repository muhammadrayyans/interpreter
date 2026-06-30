import numpy as np # type: ignore
from config.config import TokenType, keyword, OperatorType
import cython as c
from typing import Any

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
def tokenize_var(token_list: list) -> list:
    
    # creating temporary space for storing value
    token_list_return = []
    # skip index for skipping un necessary loops
    skip_index: list = []
    # calling the token abstract tree as class obj
    token_converter: object = Tokenization
    #looping through the list witch was formatted
    # formatting the loop with filters
    token_list = [x for x in token_list if x not in [' ', '']]
    token_list = ['`' if x == "'" else x for x in token_list]
    
    index: c.int
    x: Any
    limit: c.int = len(token_list)
    
    for index in range(limit):
        x = token_list[index]
        
        # skipping if skip index exist or the sting is completely empty
        if np.isin(skip_index, index).any() or x == '' or x == " ":
            # adding the elements to the token even if skipped
            continue
        
        # using try catch block for safety and catching errors
        try:
            # checking if token value exist for provided keyword if none raise error
            if keyword.get(x.replace(' ', '')) != None:
                if x == '=' and token_list[index+1] == '=':
                    token_list_return.append(OperatorType.COMPARISON.name)
                    skip_index.append(index+1)
                elif x == '=' and token_list[index-1] == '!':
                    token_list_return.pop(len(token_list_return)-1)
                    token_list_return.append(OperatorType.NOT_EQUAL.name)
                elif x == '=' and token_list[index-1] == '<':
                    token_list_return.pop(len(token_list_return)-1)
                    token_list_return.append(OperatorType.LESSER_THAN_EQUAL.name)
                elif x == '=' and token_list[index-1] == '>':
                    token_list_return.pop(len(token_list_return)-1)
                    token_list_return.append(OperatorType.GREATER_THAN_EQUAL.name)
                else:
                    # else get the corresponding data to temp storage
                    token_list_return.append(keyword[x.replace(' ' ,'')].name)

            else : raise KeyError  
        # excepting the key error and using the variable itself as the token witch is essential for variable declaration
        except KeyError:
            token_list_return.append(x)
            
    # returning the tokenized list
    return token_list_return

@c.wraparound(False)
@c.boundscheck(False)
# numeric list for better performance
def numeric_var(token_list: list) -> list[int]:
    
    numeric_list: list = []
    limit: c.int = len(token_list)
    index: c.int
    
    for index in range(limit):
        i  = token_list[index]
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
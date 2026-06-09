from enum import Enum, auto
from tree import variable_tree
from utils import debug, generate_index
import numpy as np # type: ignore

# enums for all keywords from python 
class TokenType(Enum):

    NUMBER = auto()     # 123
    IDENTIFIER = auto() # variable names like 'x' or 'total'
    STRING = auto()     # "hello"

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    INPUT = auto()
    FOR = auto()
    PARENTHESIS_OPEN = auto()
    BRACKETS_OPEN = auto()
    CURLY_BRACE_OPEN = auto()
    PARENTHESIS_CLOSE = auto()
    BRACKETS_CLOSE = auto()
    CURLY_BRACE_CLOSE = auto()
    COMMA = auto()
    DOT = auto()
    QUOTE = auto()
    SPACE = auto()
    EQUAL = auto()

    EOF = auto()

# keywords from language mapped to enums  
keyword = {
    "assume": TokenType.IF,
    "otherwise": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "display": TokenType.PRINT,
    "get": TokenType.INPUT,
    "{":TokenType.CURLY_BRACE_OPEN,
    '}':TokenType.CURLY_BRACE_CLOSE,
    '(':TokenType.PARENTHESIS_OPEN,
    ')':TokenType.PARENTHESIS_CLOSE,
    '[':TokenType.BRACKETS_OPEN,
    ']':TokenType.BRACKETS_CLOSE,
    '.':TokenType.DOT,
    ',':TokenType.COMMA,
    '"':TokenType.QUOTE,
    ' ':TokenType.SPACE,
    '=':TokenType.EQUAL
}


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
        
        if np.isin(skip_index, index).any():
            # adding the elements to the token even if skipped
            continue
        
        # using try catch block for safety and catching errors
        try:
            # checking if token value exist for provided keyword if none raise error
            match token_converter.token_value(keyword[x]):
                case None:
                    raise KeyError
                # else get the corresponding data to temp storage
                case _:
                    token_list.append(token_converter.token_value(keyword[x]))
        # exerting the key error and using the variable itself as the token witch is essential for variable declaration
        except KeyError:
            # checking list size to reduce error if it doesn't 
            # start with quotes amd the next element is '=' assuming its a variable
            # included nested check with list wrap to find exact next element to compare if its equal
            if index+1 < len(list) and  x[0] != '"' and token_converter.token_value(keyword[list[index+1]]) == TokenType.EQUAL.value:
                # creating variable object
                variable_object = variable_tree(x, x[index+2])
                # calling set value function 
                variable_object.create_variable()
                # adding the var itself
                token_list.append(x)
                # adding the ='s numeric value
                token_list.append(TokenType.EQUAL.value)
                # adding the value that's assigned to the variable
                token_list.append(list[index+2])
                #adding skip index of the '=' and value
                skip_index.extend(generate_index(index+1, index+3))
            else:
                # added normal strings
                token_list.append(x)
            
    # returning the tokenized list
    return token_list
    
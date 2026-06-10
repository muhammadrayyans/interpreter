from memory_function import set_memory, get_memory
from utils import debug, generate_index
from config import keyword, TokenType
import numpy as np # type: ignore

# class for var tree
class VariableTree:
    # constructor with basic var need gest index of =
    def __init__(self, token_list : list, index : int):
        self.token_list = token_list
        self.index = index
        self.name = self.token_list[self.index-1]
        self.index = index
    
    # var creation function witch run automatically
    def set_variable(self) -> tuple[str, list]:
        # index is of the '=' sign var is index1 and value is index-1
        # loop control var to track of loop count
        loop_control = 0
        # adds all var to this
        variable_addition = ''
        # added value of each element as number using keyword
        keyword_dict = keyword[self.token_list[self.index + loop_control]]
        # to track of skip numbers
        skip_list = []
        global_skip_list = []
        # while loop for var addition
        while self.index+loop_control <= len(self.token_list) and keyword_dict != TokenType.NEWLINE:
            # skip list checking
            if np.isin(skip_list, self.index+loop_control).any():
                loop_control+=1
                # updating value of keyword dict after each count inside skipper
                keyword_dict = keyword[self.token_list[self.index + loop_control]]
                continue
            elif keyword_dict != -1:
                if keyword_dict.value == 14: 
                    # +1 for finding the value witch is after '{'
                    value = get_memory(self.token_list[self.index + loop_control + 1])
                    # adding tht value to temp var
                    variable_addition+=str(value)
                    # skipping next 2 index witch is the var and '}'
                    skip_list.extend(generate_index(self.index+loop_control+1, self.index+loop_control+3))
            else:
                # checking if token val not equal to nine so it wont return error or ty to add it
                if self.index+loop_control < len(self.token_list) and self.token_list[self.index+loop_control] != None:
                    # if index not in skip index and the key is not '{' adding string directly to temp var
                    variable_addition+=self.token_list[self.index+loop_control]
            loop_control+=1
            # updating value of keyword dict after each count 
            # try and except block for key error which try's to access non existing value on enum
            try:
                if self.index+loop_control < len(self.token_list):
                    keyword_dict = keyword[self.token_list[self.index + loop_control]]
                else:
                    continue
            except KeyError:
                # if fall back to key error set value as -1 so loop wont stop and run
                keyword_dict = -1
        # adding the start index to stop index in global skip so they dont bother tracking
        global_skip_list.extend(generate_index(self.index, self.index+loop_control))
        # removing space from var
        self.name = self.name.replace(' ', '')
        # adding var to memory
        set_memory(self.name, variable_addition)
        # returning the result
        return variable_addition, global_skip_list
    
    def get_variable(self):
        pass
        
    

    
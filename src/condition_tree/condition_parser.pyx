from modules.condition_extractor import ConditionExtractor
from modules.condition_scope import ConditionScopeFinder
import numpy as np # type: ignore
import config.config as config
from config.config import TokenType, scope_var
from typing import Any
import logging
logger = logging.getLogger(' condition_parser')
logger.setLevel(logging.DEBUG)
from modules.env_parser import EnvParser as Parser
from utils.utils import generate_index
import random 


class ConditionParser:
    """A class tht evaluates condition and execute sub classes
    
    Args:
        index: the index of the **assume** statement
        numeric_list: the numerical tokenized list of source code
        token_list: keyword based tokenized list of source code
        exe_index: index of execution list where we want to add the in-scope execution nodes
    """
    
    def __init__(self, index: int, numeric_list: list, token_list: list[Any], scope=None) -> None:
        self.index = index
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.scope = scope
    
    
    def __scope_name_generator(self):
        return_val = random.randint(4000, 14000)
        if return_val in scope_var:
            return_val = random.randint(4000, 1004000)
            while return_val in scope_var:
                return_val = random.randint(4000, 1004000)
                 
        config.scope_var.append(return_val)
        return '__xJF4$N'+str(return_val)
    
    def execute(self) -> None | bool:
        # skip index for performance
        skip_index: list = []
        # condition value object witch gives the truth value on execution
        var_name = self.__scope_name_generator()
        # the starting scope 'assume'
        start_index: c.int # type: ignore
        stop_index: c.int # type: ignore        
        condition_value_obj = ConditionExtractor(self.index, self.numeric_list, self.token_list, self.scope)
        truth_value: bool = condition_value_obj.execute()
        # scope obj finder witch gives the starting and ending of the scope of 'assume'
        scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
        start_index, stop_index = scope_obj.execute()
        # id_generator: int
        # if it return true means 'assume' condition was true
        if truth_value:
            # gives the token splitted index of the token list and pass it to sub env_parser
            environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index], var_name)
            run_time: list = environment_parser_obj.execute()
            # executes the fetched parser process on execution
            for i in run_time:
                if i == False: 
                    return False
                if i == True:
                    return True
                    continue
                else:
                    i.execute()
            # extending the skip index 
            skip_index.extend(generate_index(start_index, stop_index))
        
        # if the 'assume' statement turns false
        else:
            loop_count: int = 0
            isDone: bool = False
            # loops through the 'assume' tokens linked keys like 'suppose' and 'unless' until it reach the end of 'unless'
            while self.index+loop_count+1 < len(self.numeric_list) and not isDone:
                i: Any = self.token_list[self.index+loop_count]

                if np.isin(skip_index, self.index+loop_count).any():
                    loop_count+=1
                    continue
                # if it turns to be an 'suppose' statement then create the env_parser
                # then runs the env_parser if the 'suppose' statement turns true else pass to 
                # unless if exists
                elif i == TokenType.ELIF_CONDITION.name and not isDone:
                    start_index: c.int # type: ignore
                    stop_index: c.int # type: ignore
                    # gets the truth value of the suppose statement
                    condition_value_obj = ConditionExtractor(self.index+loop_count, self.numeric_list, self.token_list, self.scope)
                    truth_value: bool = condition_value_obj.execute()
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    start_index, stop_index = scope_obj.execute()
                    skip_index.extend(generate_index(start_index, stop_index))
                    if not truth_value:
                        loop_count+=1
                        continue
                    environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index], var_name)
                    run_time: list = environment_parser_obj.execute()
                    # runs the executable's if the truth value is true
                    # executes the fetched parser process on execution
                    for i in run_time:
                        if i == False: 
                            return False
                        if i == True:
                            return True
                        else:
                            i.execute()
                    isDone = True
                    break
                # if it was 'unless' that falls back then execute whats inside its scope
                elif i == TokenType.ELSE_CONDITION.name and not isDone:
                    start_index: c.int # type: ignore
                    stop_index: c.int # type: ignore
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    start_index, stop_index = scope_obj.execute()
                    environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index], var_name)
                    run_time: list = environment_parser_obj.execute()
                    # executes the fetched parser process on execution
                    for i in run_time:
                        if i == False: 
                            return False
                        if i == True:
                            return True
                        else:
                            i.execute()
                    skip_index.extend(generate_index(start_index, stop_index))
                    break
                    
                loop_count+=1
                
        
        
    # create's a global skip that return the skip elements to be skipped
    def global_skip_index(self) -> list:
        int_end: c.int = 0 # type: ignore
        loop_count: c.int = 0 # type: ignore
        depth: c.int = 0 # type: ignore
        while self.index+loop_count < len(self.numeric_list):
            if self.token_list[self.index+loop_count] == TokenType.IF_CONDITION.name:
                depth+=1
            if self.token_list[self.index+loop_count] == TokenType.ELSE_CONDITION.name:
                if depth == 1:
                    in_loop_count: c.int = 0 # type: ignore
                    while True:
                        if self.token_list[self.index+loop_count+in_loop_count] == TokenType.CURLY_BRACE_CLOSE.name:
                            int_end = self.index+loop_count+in_loop_count
                            break
                        in_loop_count+=1
                    break
                else: depth-=1
            loop_count+=1
        
        scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
        start_index, stop_index = scope_obj.execute()
        end_int: int = stop_index if int_end == 0 else int_end
        # returns the generated skip index
        return generate_index(start_index, end_int)



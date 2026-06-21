from modules.condition_extractor import ConditionExtractor
from modules.condition_scope import ConditionScopeFinder
import numpy as np # type: ignore
import config.config as config
from config.config import TokenType
from typing import Any
import logging
logger = logging.getLogger(' condition_parser')
logger.setLevel(logging.DEBUG)
from modules.env_parser import EnvParser as Parser
from utils.utils import generate_index

class ConditionParser:
    """A class tht evaluates condition and execute sub classes
    
    Args:
        index: the index of the **assume** statement
        numeric_list: the numerical tokenized list of source code
        token_list: keyword based tokenized list of source code
        exe_index: index of execution list where we want to add the in-scope execution nodes
    """
    
    def __init__(self, index: int, numeric_list: list, token_list: list[Any]) -> None:
        self.index = index
        self.numeric_list = numeric_list
        self.token_list = token_list
    
    def execute(self) -> None:
        skip_index: list = []
        
        condition_value_obj = ConditionExtractor(self.index, self.numeric_list, self.token_list)
        truth_value: bool = condition_value_obj.execute()
        
        if truth_value:
            start_index: int
            stop_index: int
            scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
            start_index, stop_index = scope_obj.execute()
            environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index])
            run_time: list = environment_parser_obj.execute()
            for i in run_time:
                i.execute()
            skip_index.extend(generate_index(start_index, stop_index))
        
            
        else:
            loop_count: int = 0
            isDone: bool = False
            while self.index+loop_count+1 < len(self.numeric_list):
                i: Any = self.token_list[self.index+loop_count]
                if np.isin(skip_index, self.index+loop_count).any():
                    loop_count+=1
                    continue
                
                elif i == TokenType.ELIF_CONDITION.name and not isDone:
                    start_index: int
                    stop_index: int
                    condition_value_obj = ConditionExtractor(self.index+loop_count, self.numeric_list, self.token_list)
                    truth_value: bool = condition_value_obj.execute()
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    start_index, stop_index = scope_obj.execute()
                    skip_index.extend(generate_index(start_index, stop_index))
                    if not truth_value:
                        loop_count+=1
                        continue
                    environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index])
                    run_time: list = environment_parser_obj.execute()
                    for i in run_time:
                        i.execute()
                    isDone = True
                    break
                    
                elif self.token_list[self.index+loop_count+1] == TokenType.ELSE_CONDITION.name and not isDone:
                    start_index: int
                    stop_index: int
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    start_index, stop_index = scope_obj.execute()
                    environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index])
                    run_time: list = environment_parser_obj.execute()
                    for i in run_time:
                        i.execute()
                    skip_index.extend(generate_index(start_index, stop_index))
                    break
                    
                loop_count+=1
                
        
        
        
    def global_skip_index(self) -> list:
        int_end: int = 0
        loop_count: int = 0
        depth: int = 0
        while self.index+loop_count < len(self.numeric_list):
            if self.token_list[self.index+loop_count] == TokenType.IF_CONDITION.name:
                depth+=1
            if self.token_list[self.index+loop_count] == TokenType.ELSE_CONDITION.name:
                if depth == 1:
                    in_loop_count: int = 0
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
        return generate_index(start_index, end_int)



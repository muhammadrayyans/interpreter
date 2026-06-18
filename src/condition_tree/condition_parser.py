from condition_extractor import ConditionExtractor
from condition_scope import ConditionScopeFinder
import numpy as np # type: ignore
import config.config as config
from config.config import TokenType
from typing import Any
import logging
logger = logging.getLogger(' condition_parser')
logger.setLevel(logging.DEBUG)
from modules.parser import Parser # type: ignore
from utils.utils import generate_index

class ConditionParser:
    """A class tht evaluates condition and execute sub classes
    
    Args:
        index: the index of the **assume** statement
        numeric_list: the numerical tokenized list of source code
        token_list: keyword based tokenized list of source code
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
            environment_parser_obj.execute()
        
            skip_index.extend(generate_index(start_index, start_index))
            
        else:
            loop_count: int = 0
            isNext: bool = True
            while self.index+loop_count+1 < len(self.numeric_list) and self.token_list[self.index+loop_count+1] != TokenType.ELSE_CONDITION.name:
                i: Any = self.token_list[self.index+loop_count]
                if np.isin(skip_index, self.index+loop_count):
                    loop_count+=1
                    continue
                elif i == TokenType.ELIF_CONDITION and isNext:
                    start_index: int
                    stop_index: int
                    condition_value_obj = ConditionExtractor(self.index+loop_count, self.numeric_list, self.token_list)
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    truth_value: bool = condition_value_obj.execute()
                    start_index, stop_index = scope_obj.execute()
                    if truth_value:
                        environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index])
                        environment_parser_obj.execute()
                        skip_index.extend(generate_index(start_index, start_index))
                else:
                    start_index: int
                    stop_index: int
                    scope_obj = ConditionScopeFinder(self.numeric_list, self.token_list, self.index+loop_count)
                    start_index, stop_index = scope_obj.execute()
                    environment_parser_obj = Parser(self.token_list[start_index:stop_index], self.numeric_list[start_index:stop_index])
                    environment_parser_obj.execute()
                    skip_index.extend(generate_index(start_index, start_index))
                    
                loop_count+=1
                
        
        
        
    



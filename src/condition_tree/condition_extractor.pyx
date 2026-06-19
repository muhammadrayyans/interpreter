from config.config import TokenType, OperatorType, reverse_keyword
from typing import Any
import logging
from utils.utils import generate_index
from config.memory_config import get_memory
import numpy as np # type: ignore
logger = logging.getLogger(' condition_extractor')
logger.setLevel(logging.DEBUG)
from modules.calculation import CalculationLib # type: ignore
from modules.evaluator_node import EvaluatorNode # type: ignore
import cython as c

class ConditionExtractor:
    """A class tht gets both arguments and operation to be conducted
    
    Args:
        index: the index of the **assume** statement
        numeric_list: the numerical tokenized list of source code
        token_list: keyword based tokenized list of source code
    """
    
    def __init__(self, index: int, numeric_list: list, token_list: list[Any]) -> None:
        self.index = index+2
        self.numeric_list = numeric_list
        self.token_list = token_list
        
        self.condition_left: Any = None
        self.condition_right: Any = None
        self.operator: OperatorType = OperatorType.COMPARISON
    
    def __condition_extractor(self) -> tuple[Any , OperatorType, Any]:
        
        array: list = self.token_list
        limit: int = len(self.numeric_list[self.index :])
        index: int
        isCondition_entered: bool = False
        skip_index: list = []
        
        for index in range(limit):
            index+=self.index
            # i's value setting using index gotten
            i = array[index].replace(' ','')
            # if i value is of end type
            if i == TokenType.NEWLINE.name: break
            elif i == TokenType.PARENTHESIS_CLOSE.name: break
            
            # skipping
            elif np.isin(skip_index, index).any():
                continue
            
            # if the left/right value is numerical
            elif i.isdigit():
                
                # checking if i is digit 
                if index+2 < len(self.numeric_list) and self.token_list[index+2].isdigit():
                    calculation_object = CalculationLib(index, TokenType.CURLY_BRACE_OPEN.name, self.token_list)
                    skip_list, result = calculation_object.execute()
                        
                    # checking if the condition belongs to left side or right side
                    if not isCondition_entered:
                        self.condition_left = result
                    elif isCondition_entered:
                        self.condition_right = result
                        
                    # generating the skip index
                    skip_index.extend(skip_list)
                else:
                    if "." in i:
                        result = float(i)
                    else:
                        result = int(i)
                        
                    # checking if the condition belongs to left side or right side
                    if not isCondition_entered:
                        self.condition_left = result
                    elif isCondition_entered:
                        self.condition_right = result
                    
                
            # if the left/right value is string 
            elif i in [TokenType.QUOTE.name, TokenType.FORMAT.name] and self.token_list[index+2] in [TokenType.QUOTE.name, TokenType.FORMAT.name]:
                if not isCondition_entered:
                    self.condition_left = str(self.token_list[index+1])
                    skip_index.extend(generate_index(index, index+3))
                elif isCondition_entered:
                    self.condition_right = str(self.token_list[index+1])
                    skip_index.extend(generate_index(index, index+3))
            
            # if the i value is of operator type
            elif i == OperatorType.COMPARISON.name:
                isCondition_entered = True
                self.operator = OperatorType.COMPARISON
            elif i == OperatorType.NOT_EQUAL.name:
                isCondition_entered = True
                self.operator = OperatorType.NOT_EQUAL
            elif i == OperatorType.LESSER_THAN.name:
                self.operator = OperatorType.LESSER_THAN
                isCondition_entered = True
            elif i == OperatorType.GREATER_THAN.name:
                self.operator = OperatorType.GREATER_THAN
                isCondition_entered = True
            elif i == OperatorType.LESSER_THAN_EQUAL.name:
                self.operator = OperatorType.LESSER_THAN_EQUAL
                isCondition_entered = True
            elif i == OperatorType.GREATER_THAN_EQUAL.name:
                self.operator = OperatorType.GREATER_THAN_EQUAL
                isCondition_entered = True
            
            # if i value is a variable
            else:
                condition_value = get_memory(i)
                # if the value belongs to right side
                if not isCondition_entered:
                    self.condition_left = condition_value
                # if the value belongs to left side
                elif isCondition_entered:
                    self.condition_right = condition_value
        
        return self.condition_right, self.operator, self.condition_left
      
    @c.wraparound(False)
    @c.boundscheck(False)
    def execute(self) -> bool:
        right_condition, operator, left_condition = self.__condition_extractor()
        evaluation_obj = EvaluatorNode(left_condition, operator, right_condition)
        result: bool = evaluation_obj.execute()
        return result
        
        
    



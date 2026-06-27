import config.config as config
from config.config import OperatorType
from typing import Any
import logging 
logger = logging.getLogger(' evaluator_node')
logger.setLevel(logging.DEBUG)
from colorama import Fore # type: ignore
import cython as c

class EvaluatorNode:
    """A class that evaluate the provided condition with provided operator
    
    Args:
        left_condition: the condition on the left side
        operator: the operator witch is to be used to evaluate these condition
        right_condition: the condition on the right side
    """
    
    
    def __init__(self, left_condition: Any, operator: OperatorType, right_condition: Any) -> None:
        self.left_condition = left_condition
        self.operator = operator
        self.right_condition = right_condition
        self.return_value: bool
    
    @c.wraparound(False)
    @c.boundscheck(False)
    def execute(self) -> bool:
        
        try:
            if type(self.left_condition) == type(self.right_condition):
                # if operator is comparison
                if self.operator == OperatorType.COMPARISON:
                    if self.left_condition == self.right_condition:
                        self.return_value = True
                    else: self.return_value = False
                # if operator is '!='
                elif self.operator == OperatorType.NOT_EQUAL:
                    if self.left_condition != self.right_condition:
                        self.return_value = True
                    else: self.return_value = False
                
                # checks if its numeric because < > operators can only be apply in numeric values
                elif isinstance((self.left_condition), int) or isinstance((self.left_condition), float):
                    # if operator is >
                    if self.operator == OperatorType.GREATER_THAN:
                        if self.left_condition > self.right_condition:
                            self.return_value = True
                        else: self.return_value = False
                    # if operator is <
                    elif self.operator == OperatorType.LESSER_THAN:
                        if self.left_condition < self.right_condition:
                            self.return_value = True
                        else: self.return_value = False
                    # if operator is >=
                    elif self.operator == OperatorType.GREATER_THAN_EQUAL:
                        if self.left_condition >= self.right_condition:
                            self.return_value = True
                        else: self.return_value = False
                    # if operator is '<=
                    elif self.operator == OperatorType.LESSER_THAN_EQUAL:
                        if self.left_condition <= self.right_condition:
                            self.return_value = True
                        else: self.return_value = False
                        
                
            # raising key error for un matched comparison
            else: raise TypeError
        
        # excepting a type error for comparison b/w different types
        except TypeError:
            logging.error(Fore.RED+f" Type of compared variables are different'\033[4m\033[1m{self.left_condition} and {self.right_condition}\033[0m")
            config.isError = True
        
        # returning the evaluation result
        return self.return_value
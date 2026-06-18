from config.config import OperatorType
from typing import Any
import logging 
logger = logging.getLogger(' evaluator_node')
logger.setLevel(logging.DEBUG)

class EvaluatorNode:
    
    def __init__(self, left_condition: Any, operator: OperatorType, right_condition: Any) -> None:
        self.left_condition = left_condition
        self.operator = operator
        self.right_condition = right_condition
        
    def execution(self):
        
        if self.operator == OperatorType.COMPARISON:
            pass
        elif self.operator == OperatorType.NOT_EQUAL:
            pass
        elif self.operator == OperatorType.GREATER_THAN:
            pass
        elif self.operator == OperatorType.LESSER_THAN:
            pass
        elif self.operator == OperatorType.GREATER_THAN_EQUAL:
            pass
        elif self.operator == OperatorType.LESSER_THAN_EQUAL:
            pass
        pass
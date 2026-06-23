from modules.condition_extractor import ConditionExtractor 
from modules.condition_scope import ConditionScopeFinder
from modules.env_parser import EnvParser
import logging 
logger = logging.getLogger(' loop_parser')
logger.setLevel(logging.DEBUG)

class LoopParser:
    """A class that parse while loop exe element and run based on condition
    
    Args:
        index: index of the '' keyword
        numeric_list: the numerical tokenized list of source code
        token_list: keyword based tokenized list of source code
        scope: the scope depth in var terms
    """
    
    def __init__(self, index: int, numeric_list: list, token_list: list, scope=None) -> None:
        self.index = index
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.scope = scope
        
    def execute(self):
        scope_area = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
        start_val, stop_val = scope_area.execute()
        truth_value: bool = True
        isDone: bool = False
        condition_executer_obj = ConditionExtractor(self.index, self.numeric_list, self.token_list, self.scope)
        env_run = EnvParser(self.token_list[start_val:stop_val], self.numeric_list[start_val:stop_val], self.scope)
        executer = env_run.execute()
        
        while truth_value and not isDone:
            
            
            if not truth_value:
                isDone = True
                break
            
            else:
                for exe in executer:
                    # check for break statement
                    if exe == False:
                        break
                    elif exe == True:
                        continue
                    exe.execute()
                    
            truth_value = condition_executer_obj.execute()
        
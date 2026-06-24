from modules.condition_extractor import ConditionExtractor 
from modules.condition_scope import ConditionScopeFinder
from modules.env_parser import EnvParser
from utils.utils import generate_index
import numpy as np # type: ignore
from config.config import scope_var
import config.config as config
import logging 
import random
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
        
    def __scope_name_generator(self):
        return_val = random.randint(4000, 14000)
        if return_val in scope_var:
            return_val = random.randint(4000, 1004000)
            while return_val in scope_var:
                return_val = random.randint(4000, 1004000)
                 
        config.scope_var.append(return_val)
        return '__xJF4$N'+str(return_val)
        
    def execute(self):
        
        var_name = self.__scope_name_generator()
        scope_area = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
        start_val, stop_val = scope_area.execute()
        truth_value: bool = True
        isDone: bool = False
        condition_executer_obj = ConditionExtractor(self.index, self.numeric_list, self.token_list, self.scope)
        env_run = EnvParser(self.token_list[start_val:stop_val], self.numeric_list[start_val:stop_val], var_name)
        executer = env_run.execute()
        
        while truth_value and not isDone:
            
            if not truth_value:
                isDone = True
                break
            
            else:
                in_skip: list = []
                loop_count_for = 0
                for exe in executer:
                    
                    if np.isin(in_skip, loop_count_for).any():
                        loop_count_for+=1
                        continue
                    
                    # check for break statement
                    if exe == False:
                        isDone = True
                        break
                    
                    elif exe == True:
                        continue
                    else:
                        return_none = exe.execute()
                        if return_none == False:
                            isDone = True
                            break
                        elif return_none == True:
                            in_skip.append(loop_count_for+1)
                    loop_count_for+=1
                    
            if isDone:
                truth_value = False 
                break
            else: 
                truth_value = condition_executer_obj.execute()
                
    def global_skip(self) -> list:
        scope_area = ConditionScopeFinder(self.numeric_list, self.token_list, self.index)
        start_val, stop_val = scope_area.execute()
        return generate_index(start_val, stop_val)
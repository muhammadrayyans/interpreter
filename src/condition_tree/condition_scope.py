from config.config import TokenType
import logging
from modules.parser import Parser # type: ignore
logger = logging.getLogger(' condition_scope')
logger.setLevel(logging.DEBUG)

class ConditionScopeFinder:
    """A class that finds and create an execution node for 'assume' functions scope as start and stop index
    
    Args:
        numeric_list: the numerical tokenized list of source code
        token_list: self.index word based tokenized list of source code
        index: the index of 'assume statement witch was registered'
        scope_start (function variable): gives the starting, the '{'
        scope_end (function variable): gives the end, '}'
    """
    
    def __init__(self, numeric_list: list, token_list: list, index: int) -> None:
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.index = index
        self.scope_start: int
        self.scope_end: int
    
    def execute(self) -> tuple[int, int]:
        
        loop_count: int = 0
        isNext: bool = False
        
        # finding the scope of 'assume'
        while self.token_list[self.index+loop_count] != TokenType.CURLY_BRACE_CLOSE.name:
            
            # triggering in b/w true and false so it doesn't stumble up on nested loop 
            # then sets the start scope start and scop end of 'assume'
            if self.token_list[self.index+loop_count] == TokenType.CURLY_BRACE_OPEN.name:
                if not isNext:
                    self.scope_start = self.index+loop_count
                isNext = not isNext
                
            elif self.token_list[self.index+loop_count+1] == TokenType.CURLY_BRACE_CLOSE.name:
                if isNext:
                    self.scope_end = self.index+loop_count+1
                isNext = not isNext
                
        # return the starting and ending            
        return self.scope_start, self.scope_end
    
    

            
            
        
            
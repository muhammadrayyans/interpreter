from config.config import TokenType
from config.memory_config import set_memory
import modules.output_tree as Display
import logging
logger = logging.getLogger(' input')
logger.setLevel(logging.DEBUG)

class Get:
    def __init__(self, numeric_list: list[int], token_list: list[any], index: int):
        self.numeric_list = numeric_list
        self.token_list = token_list
        self.index = index
        
    def execute(self):
        var_name: str = self.token_list[self.index-2]
        var_name = var_name.replace(' ', '')
        if self.numeric_list[self.index+1] == TokenType.PARENTHESIS_OPEN and self.numeric_list[self.index+2] != TokenType.PARENTHESIS_CLOSE:
            display_obj = Display(self.numeric_list, self.token_list, self.index)
            display_obj.execute()
        value = input()
        set_memory(var_name, value)
        

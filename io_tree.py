from tree import VariableTree
from utils import debug

class Display:
    
    def __init__(self, list: list, index: int):
        self.index = index
        self.token_list = list
    def execute(self) -> list[int]:
        debug(self.token_list,"list")
        variable_obj = VariableTree(self.token_list, self.index)
        result, skip_index = variable_obj.set_variable()
        print(result)
        return skip_index
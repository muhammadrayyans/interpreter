from tree import VariableTree
from utils import debug

class Display:
    
    def __init__(self, list: list, index: int):
        self.index = index+2
        self.token_list = list
        
    def execute(self) -> list[int]:
        split_list = []
        for i in self.token_list[self.index :]:
            if i != '`':
                split_list.append(i)
        debug("split list", split_list)
        variable_obj = VariableTree(split_list, self.index+2)
        result, skip_index = variable_obj.formatted_string()
        print(result)
        return skip_index
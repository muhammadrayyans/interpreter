from memory_function import set_memory, get_memory

class variable_tree:
    def __init__(self, name : str, value: any):
        self.name = name
        self.value = value
    
    def create_variable(self):
        set_memory(self.name, self.value)
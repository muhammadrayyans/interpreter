from typing import Any

class DataModule:
    """A class that store variable value and data type
    
    Args:
        variable_name: the actual name of current variable
        data: the data tht was provided for storing
        data_type: the type of the provided data (eg: str, int, bool, float ect...)
    """
    
    def __init__(self, variable_name: str, data: Any) -> None:
        
        self.variable_name = variable_name
        self.data = data
        self.data_type = type(data)
    
    def execute(self) -> tuple[str, Any, Any]:
        return self.variable_name, self.data, self.data_type
        

from typing import Any

class DataModule:
    """A class that store variable value and data type
    
    Args:
        variable_name: the actual name of current variable
        data: the data tht was provided for storing
    """
    
    def __init__(self, variable_name: str, data: Any) -> None:
        
        self.variable_name = variable_name
        self.data = data
        self.data_type = type(data)
        
    def __str__(self) -> Any: 
        return self.data
    
    def execute(self) -> tuple[str, Any, Any]:
        return self.variable_name, self.data, self.data_type
    
    def value_change(self, value: Any, isConverted: bool):
        if value.isdigit() and isConverted:
            if "." in value and self.data_type is not str:
                self.data_type = float
                self.data = float(value)
            else:
                self.data_type = int
                self.data = int(value)
                
        else:
            self.data_type = type(value)
            
        self.data = value
    
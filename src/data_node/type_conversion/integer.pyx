from config.config import TokenType
from modules.calculation import CalculationLib

class IntegerConvert:
    """A class that helps to convert Any to integer 
    Args:
        token_list: tokenized list of source code 
        index: index of element witch to be converted to int
    """
    
    def __init__(self, token_list: list, index: int) -> None:
        self.token_list = token_list
        self.index = index
        
    def execute(self) -> tuple[list, int]:
        calc_obj = CalculationLib(self.index+2, TokenType.PARENTHESIS_CLOSE.name, self.token_list)
        skip_list, return_data = calc_obj.execute()
        value = int(return_data) 
        return skip_list, value
        
    
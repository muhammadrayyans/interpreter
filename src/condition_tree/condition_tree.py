from typing import Any
import logging 
logger = logging.getLogger(' condition_tree')
logger.setLevel(logging.DEBUG)

class Condition:
    
    def __init__(self, parse_obj: Any) -> None:
        self.parse_obj = parse_obj
        
    def execute(self):
        self.parse_obj.execute()
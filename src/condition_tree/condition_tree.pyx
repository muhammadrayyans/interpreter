from typing import Any
import logging 
logger = logging.getLogger(' condition_tree')
logger.setLevel(logging.DEBUG)
import cython as c

class Condition:
    """A class that execute the condition function
    
    Args:
        parse_obj: the executable condition evaluation object
    """
    
    def __init__(self, parse_obj: Any) -> None:
        self.parse_obj = parse_obj

    @c.wraparound(False)
    @c.boundscheck(False)        
    def execute(self):
        # executing the main condition object
        self.parse_obj.execute()
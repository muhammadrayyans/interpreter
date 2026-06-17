import logging
logger = logging.getLogger(' output_tree')
logger.setLevel(logging.DEBUG)
import cython as c
from modules.display_parser import ParserDisplay

class Display:
    """A class that display the user input serving same function as 'print' function in python
    
    Args:
        print_object: its a display node that gives the content to be printed
    """
    
    # constructor for print function
    def __init__(self, print_object: ParserDisplay) -> None:
        self.print_string = print_object
        
    @c.boundscheck(False)  
    @c.wraparound(False)
    def execute(self):
        value = self.print_string.execute()
        print(value)
        
                
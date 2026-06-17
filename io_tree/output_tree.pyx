import logging
logger = logging.getLogger(' output_tree')
logger.setLevel(logging.DEBUG)
import cython as c
from modules.display_parser import ParserDisplay

class Display:
    
    # constructor for print function
    def __init__(self, print_object: ParserDisplay) -> None:
        self.print_string = print_object
        
    @c.boundscheck(False)  
    @c.wraparound(False)
    def execute(self):
        value = self.print_string.execute()
        print(value)
        
                
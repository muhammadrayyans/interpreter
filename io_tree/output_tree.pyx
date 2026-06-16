import logging
logger = logging.getLogger(' output_tree')
logger.setLevel(logging.DEBUG)
import cython as c

class Display:
    
    # constructor for print function
    def __init__(self, print_string: str) -> None:
        self.print_string = print_string
        
    @c.boundscheck(False)  
    @c.wraparound(False)
    def execute(self):
        print(self.print_string)
        
                
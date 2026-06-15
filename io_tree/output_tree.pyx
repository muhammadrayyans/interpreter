from config.config import TokenType, reverse_keyword, local_memory
from utils.utils import  generate_index
import numpy as np # type: ignore
from config.memory_config import get_memory
import logging
logger = logging.getLogger(' output_tree')
logger.setLevel(logging.DEBUG)
import cython as c
from typing import Any

class Display:
    
    # constructor for print function
    def __init__(self, print_string: str) -> None:
        self.print_string = print_string
        
    def execute(self):
        print(self.print_string)
        
                
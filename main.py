from modules.tokenization_config import tokenize_var, numeric_var 
from modules.variable_tree_config import VariableFormation
from parser.parser import Parser
import config.config as config
import time
import re

import logging
logger = logging.getLogger(' main')
logger.setLevel(logging.DEBUG)

start_time: float = time.perf_counter()

# using file method opening and reading contents into source_code
with open('main.hx', 'r', encoding="utf-8") as file:
    source_code = file.read()
    
# using re splitting up code based on criteria's
formatted_code = re.split(r'(["=,.{}()\[\]\n\'])|(?<=None )', source_code)

# passing formatted code to tokenizer for tokenizing
token_list = tokenize_var(formatted_code)
numeric_list = numeric_var(token_list)

# initializing variable formation
variable_formation = VariableFormation(token_list, numeric_list)
variable_formation.execute()

# initializing parser
parsing_token = Parser(token_list, numeric_list)
parsing_token.execute()


for executer in config.execute_thread:
    if config.isError:
        break
    else:
        executer.execute()

stop_time: float = time.perf_counter()
logger.debug(f"took {stop_time - start_time}s to compleat")
 
    
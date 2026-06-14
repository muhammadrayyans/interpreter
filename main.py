import time as dev_time # for dev
from modules.tokenization_config import tokenize_var, numeric_var 
import numpy as np # type: ignore
from modules.variable_tree_config import VariableFormation
from config.config import TokenType, local_memory
from modules.output_tree import Display
import config.config as config
import re
import logging
logger = logging.getLogger(' main')
logger.setLevel(logging.DEBUG)
from modules.input_tree import Get # type: ignore
from parser.parser import Parser

start_time = dev_time.time()

# using file method opening and reading contents into source_code
with open('main.hx', 'r', encoding="utf-8") as file:
    source_code = file.read()
    

# using re splitting up code based on criteria's
formatted_code = re.split(r'(["=,.{}()\[\]\n\'])|(?<=None )', source_code)
# passing formatted code to tokenizer for tokenizing
token_list = tokenize_var(formatted_code)
numeric_list = numeric_var(token_list)
skip_index = []

# main loop
execute_list: list = []

parse_token = Parser(token_list, numeric_list)
parse_token.execute()
if not config.isError:
    
    variable_formation = VariableFormation(token_list, numeric_list)
    variable_formation.execute()

for index, i in enumerate(numeric_list):
    if config.isError:
        break
    else:
        if np.isin(skip_index, index).any():
            continue
        else:
            match i:
                case TokenType.PRINT.value:
                    
                    display_obj = Display(numeric_list, token_list, index)
                    display_obj.validate()
                    execute_list.append(display_obj)
                    
                case TokenType.INPUT.value:
                    
                    get_obj = Get(numeric_list, token_list, index)
                    get_obj.validate()
                    execute_list.append(get_obj)
                    
                case _:
                    continue
                    
if not config.isError:
    for executer in execute_list:
        executer.execute()

    stop_time = dev_time.time()
    logger.debug(f"Took {stop_time - start_time}s")
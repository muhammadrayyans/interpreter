from config.memory_config import  set_memory, get_memory
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
from io_tree.input_tree import Get

# using file method opening and reading contents into source_code
with open('main.hx', 'r', encoding="utf-8") as file:
    source_code = file.read()
    
# using re splitting up code based on criteria's
formatted_code = re.split(r'(["=,.{}()\[\]\n\'])|(?<=None )', source_code)
# passing formatted code to tokenizer for tokenizing
token_list = tokenize_var(formatted_code)
numeric_list = numeric_var(token_list)
skip_index = []
variable_formation = VariableFormation(token_list, numeric_list)
variable_formation.execute()
logger.debug(f"memory {local_memory}")

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
                    list_var = display_obj.execute()
                    # skip_index.extend(skip_list)
                    break
                case TokenType.INPUT.value:
                    get_obj = Get(numeric_list, token_list, index)
                    get_obj.execute()
                    logger.debug(f"memory {local_memory}")
                case _:
                    pass
                    
 
    
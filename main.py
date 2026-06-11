from memory_function import  set_memory, get_memory
from tokenization_tree import tokenize_var, numeric_var
import numpy as np # type: ignore
from var_tree import VariableFormation
from config import TokenType
from io_tree import Display
from utils import debug
import config
import re

# using file method opening and reading contents into source_code
with open('main.hx', 'r', encoding="utf-8") as file:
    source_code = file.read()
    
# using re splitting up code based on criteria's
formatted_code = re.split(r'(["=,.{}()\[\]\n\'])|(?<=None )', source_code)
# passing formatted code to tokenizer for tokenizing
token_list = tokenize_var(formatted_code)
debug("token", token_list)
numeric_list = numeric_var(token_list)
skip_index = []

variable_formation = VariableFormation(token_list, numeric_list)
variable_formation.execute()

# for index, i in enumerate(numeric_list):
#     if config.isError:
#         break
#     else:
#         if np.isin(skip_index, index).any():
#             continue
#         else:
#             match i:
#                 case TokenType.PRINT.value:
#                     display_obj = Display(token_list, index)
#                     skip_list = display_obj.execute()
#                     skip_index.extend(skip_list)
#                     break
#                 case _:
#                     pass
                    
 
    
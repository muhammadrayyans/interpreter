import numpy as np # type: ignore
from memory_function import  set_memory, get_memory
from utils import debug
import config
import re
from tokenization_tree import tokenize_var

# using file method opening and reading contents into source_code
with open('main.hx', 'r', encoding="utf-8") as file:
    source_code = file.read()
    
# using re splitting up code based on criteria's
formatted_code = re.split(r'(["=,.{}()\[\]\n])|(?<=None )', source_code)
# passing formatted code to tokenizer for tokenizing
token_list = tokenize_var(formatted_code)

while config.isError != True:
    break
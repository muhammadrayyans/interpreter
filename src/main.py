from modules.tokenization_config import tokenize_var, numeric_var # type: ignore    
from modules.parser import Parser # type: ignore
from colorama import init, Fore # type: ignore
import config.config as config
import re
import sys
import os
import logging

# Force the directory containing main.py to be in the search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# static imports for pyinstaller
if False:
    import numpy
    import config.config
    import utils.utils
    import modules.integer
    import modules.condition_parser
    import modules.condition_tree
    import modules.variable_tree_config
    import modules.tokenization_config
    import modules.condition_extractor
    import modules.calculation
    import modules.display_parser
    import modules.condition_scope
    import modules.loop_parser
    import modules.memory_config
    import modules.evaluator_node
    import modules.output_tree
    import modules.data_node
    import modules.loop_tree
    import modules.get_parser
    import modules.input_tree
    import modules.env_parser
    import modules.parser

# add main run
def main():
    """Main function witch runs all sub function associated with it 
    
    Args:
        sys.argv: except a file name with .bc extension and runs it
        
    """
    # check for system argv
    if len(sys.argv) < 2:
        # if name isn't provided exit with status code 1
        logging.error(Fore.RED+f"No source file provided.")    
        sys.exit(1)
    
    
    if sys.argv[1].lower == "-v":
        print(config.version)
        sys.exit(0)
    
    # else sets the 1 index argv as file name
    source_file: str = sys.argv[1]
    
    # check if the file really exists in the root
    if not os.path.exists(source_file):
        logging.error(Fore.RED+f"The file '{source_file}' could not be found.")
        sys.exit(1)
    
    # check if the file is .bc type
    if source_file[-3:] != ".bc":
        logging.error(Fore.RED+f"file extension not supported use .bc to run file")
        sys.exit(1)
        
    # if it pass all above edge case we start the process
    try:
        # using file method opening and reading contents into source_code
        with open(source_file, 'r', encoding="utf-8") as file:
            source_code = file.read()
            
        # using re splitting up code based on criteria's
        formatted_code: list = re.split(r'(["\+\-\*\/\>\!\%\<=,.{}()\[\]\n\'])|(?<=None )', source_code)

        # passing formatted code to tokenizer for tokenizing
        token_list: list = tokenize_var(formatted_code)
        numeric_list: list = numeric_var(token_list)

        # initializing parser
        parsing_token: Parser = Parser(token_list, numeric_list)
        parsing_token.execute()

        # execute the main thread one by one
        for executer in config.execute_thread:
            if config.isError:
                break
            else:
                executer.execute()

    # check for an un-caught error and exits if one occurs
    except Exception as e:
          logging.error(Fore.RED+f" Occurred {e}")   
          sys.exit(1)

# running the code if called main
if __name__ == "__main__":
    main()
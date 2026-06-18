from condition_parser import ConditionParser
import logging 
logger = logging.getLogger(' condition_tree')
logger.setLevel(logging.DEBUG)

class Condition:
    
    def __init__(self, parse_obj: ConditionParser) -> None:
        parse_obj.execute()
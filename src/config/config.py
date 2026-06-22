from enum import Enum, auto

# the main memory for var storage
local_memory: dict = {}

# symbol table
scope_var: list = []

# the key witch is used to control the flow of code
isError: bool = False

# enums for all keywords from python 
class TokenType(Enum):

    IF_CONDITION = auto()
    ELSE_CONDITION = auto()
    ELIF_CONDITION = auto()
    WHILE = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    INPUT = auto()
    FOR = auto()
    PARENTHESIS_OPEN = auto()
    BRACKETS_OPEN = auto()
    CURLY_BRACE_OPEN = auto()
    PARENTHESIS_CLOSE = auto()
    BRACKETS_CLOSE = auto()
    CURLY_BRACE_CLOSE = auto()
    COMMA = auto()
    DOT = auto()
    QUOTE = auto()
    SPACE = auto()
    EQUAL = auto()
    NEWLINE = auto()
    FORMAT = auto()

    EOF = auto()

# enum for all operators
class OperatorType(Enum):
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    MODULO = auto()
    COMPARISON = auto()
    GREATER_THAN = auto()
    LESSER_THAN = auto()
    GREATER_THAN_EQUAL = auto()
    LESSER_THAN_EQUAL = auto()
    NOT_EQUAL = auto()
    LOGIC_AND = auto()
    LOGIC_OR = auto()
    LOGIC_NOT = auto()
    
# enum for all data type
class DataType(Enum):
    INTEGER = auto()
    DOUBLE = auto()
    FLOAT = auto()
    BOOLEAN = auto() 

# keywords from language mapped to enums  
keyword: dict = {
    "assume": TokenType.IF_CONDITION,
    "suppose": TokenType.ELIF_CONDITION,
    "unless": TokenType.ELSE_CONDITION,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "display": TokenType.PRINT,
    "get": TokenType.INPUT,
    " get": TokenType.INPUT,
    "{":TokenType.CURLY_BRACE_OPEN,
    '}':TokenType.CURLY_BRACE_CLOSE,
    '(':TokenType.PARENTHESIS_OPEN,
    ')':TokenType.PARENTHESIS_CLOSE,
    '[':TokenType.BRACKETS_OPEN,
    ']':TokenType.BRACKETS_CLOSE,
    '.':TokenType.DOT,
    ',':TokenType.COMMA,
    '"':TokenType.QUOTE,
    ' ':TokenType.SPACE,
    '=':TokenType.EQUAL,
    '\n' : TokenType.NEWLINE,
    "`": TokenType.FORMAT,
    '+': OperatorType.ADDITION,
    '-': OperatorType.SUBTRACTION,
    '*': OperatorType.MULTIPLICATION,
    '/': OperatorType.DIVISION,
    '%': OperatorType.MODULO,
    ' int': DataType.INTEGER,
    ' double': DataType.DOUBLE,
    ' float': DataType.FLOAT,
    ' bool': DataType.BOOLEAN,
    '>': OperatorType.GREATER_THAN,
    '<': OperatorType.LESSER_THAN
}

# reverse_keyword tht store the key value form keywords in opposite
reverse_keyword: dict = {
    TokenType.IF_CONDITION: "assume",
    TokenType.ELIF_CONDITION: "suppose",
    TokenType.ELSE_CONDITION: "otherwise",
    TokenType.WHILE: "while",
    TokenType.FOR: "for",
    TokenType.TRUE: "true",
    TokenType.FALSE: "false",
    TokenType.PRINT: "display",
    TokenType.INPUT: "get",
    TokenType.CURLY_BRACE_OPEN: "{",
    TokenType.CURLY_BRACE_CLOSE: "}",
    TokenType.PARENTHESIS_OPEN: "(",
    TokenType.PARENTHESIS_CLOSE: ")",
    TokenType.BRACKETS_OPEN: "[",
    TokenType.BRACKETS_CLOSE: "]",
    TokenType.DOT: ".",
    TokenType.COMMA: ",",
    TokenType.QUOTE: '"',
    TokenType.SPACE: " ",
    TokenType.EQUAL: "=",
    TokenType.NEWLINE: "\n",
    TokenType.FORMAT: "`",
    OperatorType.ADDITION: '+',
    OperatorType.SUBTRACTION:'-' ,
    OperatorType.MULTIPLICATION:'*' ,
    OperatorType.DIVISION: '/',
    OperatorType.MODULO:'%' ,
    DataType.INTEGER: 'int',
    DataType.DOUBLE: 'double',
    DataType.FLOAT: 'float',
    DataType.BOOLEAN:'bool',
    OperatorType.GREATER_THAN: '>',
    OperatorType.LESSER_THAN: '<'
}

# main skip list
config_skip_index: list = []

# main execute line
execute_thread: list = []
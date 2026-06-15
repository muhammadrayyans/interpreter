from enum import Enum, auto

# the main memory for var storage
local_memory: dict = {}

# the key witch is used to control the flow of code
isError: bool = False


# enums for all keywords from python 
class TokenType(Enum):

    NUMBER = auto()     # 123
    IDENTIFIER = auto() # variable names like 'x' or 'total'
    STRING = auto()     # "hello"

    IF = auto()
    ELSE = auto()
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
    
# keywords from language mapped to enums  
keyword: dict = {
    "assume": TokenType.IF,
    "otherwise": TokenType.ELSE,
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
    "`": TokenType.FORMAT
}

reverse_keyword: dict = {
    TokenType.IF: "assume",
    TokenType.ELSE: "otherwise",
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
    TokenType.FORMAT: "`"
}

# main skip list
config_skip_index: list = []

# main execute line
execute_thread: list = []
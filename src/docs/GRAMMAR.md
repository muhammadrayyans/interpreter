# Core Program Architecture
- program             ::= block
- block               ::= "{" statement* "}"

# Main Statement Dispatcher 
### statement           ::= declaration 
-  | assignment 
-  | assume_statement 
-  | suppose_statement 
-  | unless_fallback 
-  | when_statement 
-  | stop_statement 
-  | jump_statement 
-  | int_statement 
-  | display_statement 
-  | get_statement

# Structural & Control Statements
- declaration         ::= identifier
- assignment          ::= identifier "=" expression

- assume_statement    ::= "assume" "(" condition ")" block
- suppose_statement   ::= "suppose" "(" condition ")" block
- unless_fallback     ::= "unless" block
- when_statement      ::= "when" "(" condition ")" block

- stop_statement      ::= "stop"
- jump_statement      ::= "jump" identifier
- int_statement       ::= "int" "(" condition ")"

# I/O Operations
- display_statement   ::= "display" "(" expression ")"
- get_statement       ::= "get" "(" identifier ")"

# Foundational Elements (Terminals & Expressions)
- condition           ::= expression relational_operator expression
- expression          ::= term ( binary_operator term )*
- term                ::= identifier | literal

- relational_operator ::= "==" | "!=" | ">" | "<" | ">=" | "<="

- identifier          ::= [a-zA-Z_][a-zA-Z0-9_]*
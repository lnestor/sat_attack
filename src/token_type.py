from enum import Enum

class TokenType(Enum):
    EOF = 0
    COMMA = 1
    LEFT_BRACKET = 2
    RIGHT_BRACKET = 3
    BACKTICK = 4
    DIVIDE_OPERATOR = 5
    RIGHT_PAREN = 6
    LEFT_PAREN = 7
    IDENTIFIER = 8
    TIMING = 9
    SEMICOLON = 10
    TIMESCALE = 11
    MODULE = 12
    INPUT = 13
    OUTPUT = 14
    WIRE = 15
    AND = 16
    XOR = 17
    ENDMODULE = 18
    OR = 19
    NOT = 20

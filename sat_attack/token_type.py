from enum import Enum

class TokenType(Enum):
    EOF = 0

    COMMA = 1
    COLON = 2
    SEMICOLON = 3
    BACKTICK = 4
    DIVIDE_OPERATOR = 5

    LEFT_BRACKET = 6
    RIGHT_BRACKET = 7
    RIGHT_PAREN = 8
    LEFT_PAREN = 9

    IDENTIFIER = 10
    NUMBER = 11
    TIMING = 12

    TIMESCALE = 13
    MODULE = 14
    INPUT = 15
    OUTPUT = 16
    WIRE = 17
    ENDMODULE = 18

    AND = 19
    XOR = 20
    OR = 21
    NOT = 22
    NAND = 23
    XNOR = 24
    NOR = 25

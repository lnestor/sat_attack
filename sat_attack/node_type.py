from enum import Enum

class NodeType(Enum):
    NOT = 0
    BUF = 1
    AND = 2
    NAND = 3
    OR = 4
    NOR = 5
    XOR = 6
    XNOR = 7
    INPUT = 8
    OUTPUT = 9
    WIRE = 10
    CONSTANT = 11
    EQUAL = 12

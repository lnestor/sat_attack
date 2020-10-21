from enum import Enum
from token_type import TokenType

class State(Enum):
    START = 0
    GATHERING_IDENTIFIER = 1
    GATHERING_DIGITS = 9
    ERROR = 10

class Tokenizer():
    """
    Splits input files into chunks of characters called 'tokens' that
    are easier to manipulate and parse than text. A token can be many things,
    such as a keyword (module, and, etc.) or a comma, etc. Any non-separable,
    meaningful chunk is a token.
    """
    KEYWORDS = {
        "timescale": TokenType.TIMESCALE,
        "module": TokenType.MODULE,
        "input": TokenType.INPUT,
        "output": TokenType.OUTPUT,
        "wire": TokenType.WIRE,
        "and": TokenType.AND,
        "xor": TokenType.XOR,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "nand": TokenType.NAND,
        "xnor": TokenType.XNOR,
        "nor": TokenType.NOR,
        "endmodule": TokenType.ENDMODULE
    }

    def __init__(self, fobj):
        self.fobj = fobj
        self.__find_token()

    def get_token_type(self):
        """Returns the type of the current token"""
        return self.token_type

    def skip_token(self):
        """Finds the next token"""
        self.__find_token()

    def id_value(self):
        """Returns the identifier value for the current token"""
        return self.token

    def int_value(self):
        """Returns an integer of the current token"""
        return int(self.token)

    def __find_token(self):
        """Find the next token"""
        state = State.START
        self.token = ""

        while True:
            if state == State.START:
                next_char = self.fobj.read(1)

                if not next_char.isspace():
                    self.token += next_char

                if next_char == "":
                    self.token_type = TokenType.EOF
                    break
                elif next_char == ";":
                    self.token_type = TokenType.SEMICOLON
                    break
                elif next_char == ",":
                    self.token_type = TokenType.COMMA
                    break
                elif next_char == "[":
                    self.token_type = TokenType.LEFT_BRACKET
                    break
                elif next_char == "]":
                    self.token_type = TokenType.RIGHT_BRACKET
                    break
                elif next_char == "`":
                    self.token_type = TokenType.BACKTICK
                    break
                elif next_char == "/":
                    self.token_type = TokenType.DIVIDE_OPERATOR
                    break
                elif next_char == "(":
                    self.token_type = TokenType.LEFT_PAREN
                    break
                elif next_char == ")":
                    self.token_type = TokenType.RIGHT_PAREN
                    break
                elif next_char == ":":
                    self.token_type = TokenType.COLON
                    break
                elif next_char.isalpha() or next_char == "_":
                    state = State.GATHERING_IDENTIFIER
                elif next_char.isdigit():
                    state = State.GATHERING_DIGITS
                elif not next_char.isspace():
                    # Do not error if we are reading a space
                    print(next_char)
                    state = State.ERROR
            elif state == State.GATHERING_IDENTIFIER:
                next_char = self.__peek()

                if next_char.isalpha() or next_char.isdigit() or next_char == "_":
                    self.token += self.fobj.read(1)
                elif self.token in self.KEYWORDS:
                    self.token_type = self.KEYWORDS[self.token]
                    break
                else:
                    self.token_type = TokenType.IDENTIFIER
                    break
            elif state == State.GATHERING_DIGITS:
                next_char = self.__peek()

                if next_char.isalpha():
                    self.token += self.fobj.read(2)
                    self.token_type = TokenType.TIMING
                    break
                elif next_char.isdigit():
                    self.token += self.fobj.read(1)
                else:
                    self.token_type = TokenType.NUMBER
                    break
            elif state == State.ERROR:
                print("Tokenizing error: unknown character " + next_char)
                break

    def __peek(self):
        """Peek at the next character in the input file"""
        pos = self.fobj.tell()
        c = self.fobj.read(1)
        self.fobj.seek(pos)
        return c


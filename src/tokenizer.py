from enum import Enum
from token_type import TokenType

class State(Enum):
    START = 0
    GATHERING_IDENTIFIER = 1
    GATHERING_TIMING = 9
    ERROR = 10

class Tokenizer():
    KEYWORDS = {
        "timescale": TokenType.TIMESCALE,
        "module": TokenType.MODULE,
        "input": TokenType.INPUT,
        "output": TokenType.OUTPUT,
        "wire": TokenType.WIRE,
        "and": TokenType.AND,
        "xor": TokenType.XOR,
        "endmodule": TokenType.ENDMODULE
    }

    def __init__(self, fobj):
        self.fobj = fobj
        self.__find_token()

    def get_token_type(self):
        return self.token_type

    def skip_token(self):
        self.__find_token()

    def id_value(self):
        return self.token

    def __find_token(self):
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
                elif next_char.isalpha():
                    state = State.GATHERING_IDENTIFIER
                elif next_char.isdigit():
                    state = State.GATHERING_TIMING
                elif not next_char.isspace():
                    # Do not error if we are reading a space
                    state = State.ERROR
            elif state == State.GATHERING_IDENTIFIER:
                next_char = self.__peek()

                if next_char.isalpha() or next_char.isdigit():
                    self.token += self.fobj.read(1)
                elif self.token in self.KEYWORDS:
                    self.token_type = self.KEYWORDS[self.token]
                    break
                else:
                    self.token_type = TokenType.IDENTIFIER
                    break
            elif state == State.GATHERING_TIMING:
                self.token += self.fobj.read(2)
                self.token_type = TokenType.TIMING
                break
            elif state == State.ERROR:
                print("ERROR")
                break

    def __peek(self):
        pos = self.fobj.tell()
        c = self.fobj.read(1)
        self.fobj.seek(pos)
        return c


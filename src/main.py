from tokenizer import Tokenizer
from token_type import TokenType

if __name__ == "__main__":
    with open("benchmarks/sample.v") as f:
        t = Tokenizer(f)

        tt = t.get_token()

        while tt != TokenType.EOF:
            print(tt)
            t.skip_token()
            tt = t.get_token()

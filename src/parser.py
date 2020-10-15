from node import Node
from token_type import TokenType

class Parser():
    def parse(self, tokenizer):
        # self.inputs = []
        self.outputs = []
        self.nodes = {}

        while True:
            token_type = tokenizer.get_token_type()

            if token_type == TokenType.EOF:
                break
            elif token_type == TokenType.INPUT:
                self.__parse_inputs(tokenizer)
            elif token_type == TokenType.OUTPUT:
                self.__parse_outputs(tokenizer)
            elif token_type == TokenType.WIRE:
                self.__parse_wires(tokenizer)
            elif token_type == TokenType.AND:
                self.__parse_gate(tokenizer, "And")
            elif token_type == TokenType.XOR:
                self.__parse_gate(tokenizer, "Xor")
            else:
                tokenizer.skip_token()

        return self.nodes, self.outputs

    def __parse_inputs(self, tokenizer):
        tokenizer.skip_token() # input token

        while True:
            # This check is NOT robust and could be improved probably
            type = "Key Input" if "key" in tokenizer.id_value() else "Primary Input"
            self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], type)
            tokenizer.skip_token()

            if tokenizer.get_token_type() == TokenType.SEMICOLON:
                tokenizer.skip_token()
                break
            else:
                tokenizer.skip_token()

    def __parse_outputs(self, tokenizer):
        tokenizer.skip_token() # output token

        while True:
            self.outputs.append(tokenizer.id_value())
            self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Output")
            tokenizer.skip_token()

            if tokenizer.get_token_type() == TokenType.SEMICOLON:
                tokenizer.skip_token()
                break
            else:
                tokenizer.skip_token()

    def __parse_wires(self, tokenizer):
        tokenizer.skip_token() # wire token

        while True:
            self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Wire")
            tokenizer.skip_token()

            if tokenizer.get_token_type() == TokenType.SEMICOLON:
                tokenizer.skip_token()
                break
            else:
                tokenizer.skip_token()

    def __parse_gate(self, tokenizer, gate_type):
        tokenizer.skip_token() # gate token
        tokenizer.skip_token() # gate identifier token
        tokenizer.skip_token() # left paren token

        output_name = tokenizer.id_value()
        tokenizer.skip_token() # id
        tokenizer.skip_token() # comma
        input1_name = tokenizer.id_value()
        tokenizer.skip_token() # id
        tokenizer.skip_token() # comma
        input2_name = tokenizer.id_value()
        tokenizer.skip_token() # id
        tokenizer.skip_token() # comma
        tokenizer.skip_token() # semicolon

        self.nodes[output_name].inputs = [input1_name, input2_name]
        self.nodes[output_name].type = gate_type

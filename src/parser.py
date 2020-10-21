from node import Node
from token_type import TokenType

class Parser():
    def parse(self, tokenizer):
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
            elif token_type == TokenType.OR:
                self.__parse_gate(tokenizer, "Or")
            elif token_type == TokenType.NOT:
                self.__parse_gate(tokenizer, "Not")
            elif token_type == TokenType.NAND:
                self.__parse_gate(tokenizer, "Nand")
            elif token_type == TokenType.XNOR:
                self.__parse_gate(tokenizer, "Xnor")
            elif token_type == TokenType.NOR:
                self.__parse_gate(tokenizer, "Nor")
            else:
                tokenizer.skip_token()

        return self.nodes, self.outputs

    def __parse_inputs(self, tokenizer):
        tokenizer.skip_token() # input token

        while True:
            # This check is NOT robust and could be improved probably
            if "key" in tokenizer.id_value():
                self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Key Input")
            else:
                self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Primary Input")

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
            if tokenizer.get_token_type() == TokenType.SEMICOLON:
                tokenizer.skip_token() # semicolon
                break
            elif tokenizer.get_token_type() == TokenType.COMMA:
                tokenizer.skip_token() # comma
            elif tokenizer.get_token_type() == TokenType.LEFT_BRACKET:
                self.__parse_bus(tokenizer)
            else:
                self.__parse_single_wire(tokenizer)

    def __parse_bus(self, tokenizer):
        tokenizer.skip_token() # left bracket
        low_number = tokenizer.int_value()
        tokenizer.skip_token() # low number
        tokenizer.skip_token() # colon
        high_number = tokenizer.int_value()
        tokenizer.skip_token() # high value
        tokenizer.skip_token() # right bracket
        bus_name = tokenizer.id_value()
        tokenizer.skip_token() # bus name

        for i in range(high_number - low_number + 1):
            wire_name = bus_name + "__index" + str(i)
            self.nodes[wire_name] = Node(wire_name, [], "Wire")

    def __parse_single_wire(self, tokenizer):
        self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Wire")
        tokenizer.skip_token()

    def __parse_gate(self, tokenizer, gate_type):
        tokenizer.skip_token() # gate token
        tokenizer.skip_token() # gate identifier token
        tokenizer.skip_token() # left paren token

        output_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma

        inputs = []
        while True:
            if tokenizer.get_token_type() == TokenType.RIGHT_PAREN:
                tokenizer.skip_token() # right paren
                break
            elif tokenizer.get_token_type() == TokenType.IDENTIFIER:
                input_name = self.__parse_id(tokenizer)
                inputs.append(input_name)
            elif tokenizer.get_token_type() == TokenType.COMMA:
                tokenizer.skip_token() # comma
            else:
                print("Error: unexpected token type " + tokenizer.get_token_type())

        tokenizer.skip_token() # semicolon
        self.nodes[output_name].inputs = inputs
        self.nodes[output_name].type = gate_type


    def __parse_gate1(self, tokenizer, gate_type):
        tokenizer.skip_token() # gate token
        tokenizer.skip_token() # gate identifier token
        tokenizer.skip_token() # left paren token

        # output_name = tokenizer.id_value()
        # tokenizer.skip_token() # id
        output_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma
        # input_name = tokenizer.id_value()
        # tokenizer.skip_token() # id
        input_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma
        tokenizer.skip_token() # semicolon

        self.nodes[output_name].inputs = [input_name]
        self.nodes[output_name].type = gate_type

    def __parse_gate2(self, tokenizer, gate_type):
        tokenizer.skip_token() # gate token
        tokenizer.skip_token() # gate identifier token
        tokenizer.skip_token() # left paren token

        # output_name = tokenizer.id_value()
        # tokenizer.skip_token() # id
        output_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma
        # input1_name = tokenizer.id_value()
        # tokenizer.skip_token() # id
        input1_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma
        # input2_name = tokenizer.id_value()
        # tokenizer.skip_token() # id
        input2_name = self.__parse_id(tokenizer)
        tokenizer.skip_token() # comma
        tokenizer.skip_token() # semicolon

        self.nodes[output_name].inputs = [input1_name, input2_name]
        self.nodes[output_name].type = gate_type

    def __parse_id(self, tokenizer):
        id_name = tokenizer.id_value()
        tokenizer.skip_token() # id

        if tokenizer.get_token_type() == TokenType.LEFT_BRACKET:
            tokenizer.skip_token() # left bracket
            index = tokenizer.int_value()
            tokenizer.skip_token() # number
            tokenizer.skip_token() # right bracket

            return id_name + "__index" + str(index)
        else:
            return id_name


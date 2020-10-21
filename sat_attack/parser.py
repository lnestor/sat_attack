from node import Node
from token_type import TokenType

class Parser():
    def parse(self, tokenizer):
        """
        Parses circuit nodes given a list of tokens from an input verilog file.

        tokenizer: Tokenizer object for the Verilog input file
        returns: the nodes of the circuit, the names of the output nodes
        """
        self.outputs = []
        self.nodes = {}

        while True:
            token_type = tokenizer.get_token_type()

            if token_type == TokenType.EOF:
                break
            elif token_type == TokenType.INPUT:
                self._parse_inputs(tokenizer)
            elif token_type == TokenType.OUTPUT:
                self._parse_outputs(tokenizer)
            elif token_type == TokenType.WIRE:
                self._parse_wires(tokenizer)
            elif token_type == TokenType.AND:
                self._parse_gate(tokenizer, "And")
            elif token_type == TokenType.XOR:
                self._parse_gate(tokenizer, "Xor")
            elif token_type == TokenType.OR:
                self._parse_gate(tokenizer, "Or")
            elif token_type == TokenType.NOT:
                self._parse_gate(tokenizer, "Not")
            elif token_type == TokenType.NAND:
                self._parse_gate(tokenizer, "Nand")
            elif token_type == TokenType.XNOR:
                self._parse_gate(tokenizer, "Xnor")
            elif token_type == TokenType.NOR:
                self._parse_gate(tokenizer, "Nor")
            else:
                tokenizer.skip_token()

        return self.nodes, self.outputs

    def _parse_inputs(self, tokenizer):
        """
        Parses input nodes, both key and primary inputs

        tokenizer: the Tokenizer object with the verilog input
        """
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

    def _parse_outputs(self, tokenizer):
        """
        Parses output nodes

        tokenizer: the Tokenizer object with the verilog input
        """
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

    def _parse_wires(self, tokenizer):
        """
        Parses wire nodes

        tokenizer: the Tokenizer object with the verilog input
        """
        tokenizer.skip_token() # wire token

        while True:
            if tokenizer.get_token_type() == TokenType.SEMICOLON:
                tokenizer.skip_token() # semicolon
                break
            elif tokenizer.get_token_type() == TokenType.COMMA:
                tokenizer.skip_token() # comma
            elif tokenizer.get_token_type() == TokenType.LEFT_BRACKET:
                self._parse_bus(tokenizer)
            else:
                self._parse_single_wire(tokenizer)

    def _parse_bus(self, tokenizer):
        """
        Parses wire nodes that are buses

        tokenizer: the Tokenizer object with the verilog input
        """
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

    def _parse_single_wire(self, tokenizer):
        """
        Parses a single wire node

        tokenizer: the Tokenizer object with the verilog input
        """
        self.nodes[tokenizer.id_value()] = Node(tokenizer.id_value(), [], "Wire")
        tokenizer.skip_token()

    def _parse_gate(self, tokenizer, gate_type):
        """
        Parses a gate node

        tokenizer: the Tokenizer object with the verilog input
        """
        tokenizer.skip_token() # gate token
        tokenizer.skip_token() # gate identifier token
        tokenizer.skip_token() # left paren token

        output_name = self._parse_id(tokenizer)
        tokenizer.skip_token() # comma

        inputs = []
        while True:
            if tokenizer.get_token_type() == TokenType.RIGHT_PAREN:
                tokenizer.skip_token() # right paren
                break
            elif tokenizer.get_token_type() == TokenType.IDENTIFIER:
                input_name = self._parse_id(tokenizer)
                inputs.append(input_name)
            elif tokenizer.get_token_type() == TokenType.COMMA:
                tokenizer.skip_token() # comma
            else:
                print("Error: unexpected token type " + tokenizer.get_token_type())

        tokenizer.skip_token() # semicolon
        self.nodes[output_name].inputs = inputs
        self.nodes[output_name].type = gate_type

    def _parse_id(self, tokenizer):
        """
        Parses an identifier name

        tokenizer: the Tokenizer object with the Verilog input
        """
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


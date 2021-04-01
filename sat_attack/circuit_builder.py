from z3 import *

class CircuitBuilder():
    def build_miter(self, ckt0, ckt1):
        """
        Builds a miter circuit z3 representation from two smaller circuits."

        ckt0: the first half of the miter circuit
        ckt1: the second half of the miter circuit
        returns: a miter circuit z3 representation
        """
        output_xors = [Xor(ckt0.outputs()[name], ckt1.outputs()[name]) for name in ckt0.outputs()]
        diff = Or(*output_xors)
        return {"diff": diff}

    def build(self, nodes, output_names, key_suffix = "", spec_inputs = None):
        """
        Builds a circuit z3 representation from a list of nodes in the circuit.

        nodes: the nodes in the circuit
        output_names: the names of the output nodes
        key_suffix: suffix to apply to all key names
        spec_inputs: inputs to be replace by a value
        returns: a z3 representation for the outputs of the circuit
                 corresponding to the nodes passed in
        """
        self.visited_nodes = []
        self.inputs = []
        self.specified_inputs = spec_inputs
        outputs = {}

        for name in output_names:
            outputs[name] = self._build_node(nodes, name, key_suffix)

        return outputs, self.inputs

    def _build_node(self, nodes, name, key_suffix):
        """
        Returns the z3 representation for a single node.

        nodes: a list of all nodes in the circuit
        name: the name of the node to build
        key_suffix: the suffix to apply to key names
        """
        node = nodes[name]

        if name in self.visited_nodes:
            return node.z3_repr

        self.visited_nodes.append(name)

        if node.type == "Key Input":
            self._build_key(node, name, key_suffix)
        elif node.type == "Primary Input":
            self._build_input(node, name)
        else:
            fanin = [self._build_node(nodes, child_name, key_suffix) for child_name in node.inputs]
            self._build_gate(node, fanin)

        return node.z3_repr

    def _build_gate(self, node, fanin):
        """
        Sets the z3 representation for a logic gate node.

        node: the node to find the z3 representation for
        fanin: the input nodes the the node
        """
        if node.type == "and":
            node.z3_repr = And(*fanin)
        elif node.type == "xor":
            node.z3_repr = Xor(*fanin)
        elif node.type == "or":
            node.z3_repr = Or(*fanin)
        elif node.type == "not":
            node.z3_repr = Not(*fanin)
        elif node.type == "nand":
            node.z3_repr = Not(And(*fanin))
        elif node.type == "xnor":
            node.z3_repr = Not(Xor(*fanin))
        elif node.type == "nor":
            node.z3_repr = Not(Or(*fanin))
        elif node.type == "buffer" or node.type == "buf":
            node.z3_repr = Not(Not(*fanin))
        else:
            print("Unknown node type " + str(node))
            import pdb; pdb.set_trace()
            raise

    def _build_key(self, node, name, key_suffix):
        """
        Sets the z3 representation for a key input node

        node: the node to find the z3 representation for
        name: the name of the key
        key_suffix: the suffix to apply to the key
        """
        key_name = name + key_suffix

        if self.specified_inputs is not None and name in self.specified_inputs:
            node.z3_repr = self.specified_inputs[key_name]
        else:
            self.inputs.append(key_name)
            node.z3_repr = Bool(key_name)

    def _build_input(self, node, name):
        """
        Sets the z3 representation for a primary input node

        node: the node to find the z3 representation for
        name: the name of the key
        """
        if self.specified_inputs is not None and name in self.specified_inputs:
            node.z3_repr = self.specified_inputs[name]
        else:
            self.inputs.append(name)
            node.z3_repr = Bool(name)

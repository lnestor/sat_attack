from z3 import *

class CircuitBuilder():
    def build_miter(self, ckt0, ckt1):
        output_xors = [Xor(ckt0.outputs()[name], ckt1.outputs()[name]) for name in ckt0.outputs()]
        diff = Or(*output_xors)
        return {"diff": diff}

    def build(self, nodes, output_names, key_suffix = "", spec_inputs = None):
        self.visited_nodes = []
        self.inputs = []
        self.specified_inputs = spec_inputs
        outputs = {}

        for name in output_names:
            outputs[name] = self._build_node(nodes, name, key_suffix)

        return outputs, self.inputs

    def _build_node(self, nodes, name, key_suffix):
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

        if node.type == "And":
            node.z3_repr = And(*fanin)
        elif node.type == "Xor":
            node.z3_repr = Xor(*fanin)
        elif node.type == "Or":
            node.z3_repr = Or(*fanin)
        elif node.type == "Not":
            node.z3_repr = Not(*fanin)
        elif node.type == "Nand":
            node.z3_repr = Not(And(*fanin))
        elif node.type == "Xnor":
            node.z3_repr = Not(Xor(*fanin))
        elif node.type == "Nor":
            node.z3_repr = Not(Or(*fanin))
        else:
            print("Unknown node type " + str(node))

    def _build_key(self, node, name, key_suffix):
        key_name = name + key_suffix
        self.inputs.append(key_name)
        node.z3_repr = Bool(key_name)

    def _build_input(self, node, name):
        if self.specified_inputs is not None and name in self.specified_inputs:
            node.z3_repr = self.specified_inputs[name]
        else:
            self.inputs.append(name)
            node.z3_repr = Bool(name)

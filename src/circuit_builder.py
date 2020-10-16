from z3 import *

class CircuitBuilder():
    def build_miter(self, nodes, outputs):
        ckt0, p_input_names, key_input_names0 = self.build(nodes, outputs, "ckt0")
        ckt1, p_input_names, key_input_names1 = self.build(nodes, outputs, "ckt1")

        output_xors = [None] * len(ckt0)
        for i in range(len(ckt0)):
            output_xors[i] = Xor(ckt0[i], ckt1[i])

        miter_circuit = Or(*output_xors)
        return miter_circuit, p_input_names, key_input_names0 + key_input_names1

    def build(self, nodes, outputs, key_suffix = None):
        self.key_input_names = []
        self.p_input_names = []
        circuit_outputs = []

        for output_name in outputs:
            circuit_outputs.append(self.__construct(nodes, output_name, key_suffix))

        return circuit_outputs, self.p_input_names, self.key_input_names

    def __construct(self, nodes, name, key_suffix):
        node = nodes[name]
        input_names = node.inputs

        if node.type == "Key Input":
            key_name = self.__key_name(name, key_suffix)
            if key_name not in self.key_input_names:
                self.key_input_names.append(key_name)
            return Bool(key_name)
        elif node.type == "Primary Input":
            if name not in self.p_input_names:
                self.p_input_names.append(name)
            return Bool(name)

        input_logic = []
        for input_name in input_names:
            input_logic.append(self.__construct(nodes, input_name, key_suffix))

        if node.type == "And":
            return And(*input_logic)
        elif node.type == "Xor":
            return Xor(*input_logic)
        elif node.type == "Or":
            return Or(*input_logic)
        elif node.type == "Not":
            return Not(*input_logic)
        elif node.type == "Nand":
            return Not(And(*input_logic))
        elif node.type == "Xnor":
            return Not(Xor(*input_logic))
        elif node.type == "Nor":
            return Not(Or(*input_logic))
        else:
            print("Unknown node type " + str(node))

    def __key_name(self, name, key_suffix):
        if key_suffix is None:
            return name
        else:
            return name + "__" + key_suffix



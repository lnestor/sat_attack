from z3 import *

class CircuitBuilder():
    def build_miter(self, nodes, outputs):
        circuit0 = self.build(nodes, outputs, "ckt0")
        circuit1 = self.build(nodes, outputs, "ckt1")

        output_xors = [None] * len(circuit0)
        for i in range(len(circuit0)):
            output_xors[i] = Xor(circuit0[i], circuit1[i])

        miter_circuit = Or(*output_xors)
        return miter_circuit

    def build(self, nodes, outputs, key_suffix = None):
        circuit_outputs = []

        for output_name in outputs:
            circuit_outputs.append(self.__construct(nodes, output_name, key_suffix))

        return circuit_outputs

    def __construct(self, nodes, name, key_suffix):
        node = nodes[name]
        input_names = node.inputs

        if node.type == "Key Input":
            return Bool(self.__key_name(name, key_suffix))
        elif node.type == "Primary Input":
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
        else:
            print("Unknown node type " + node.type)

    def __key_name(self, name, key_suffix):
        if key_suffix is None:
            return name
        else:
            return name + "__" + key_suffix



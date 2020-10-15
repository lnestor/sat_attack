from z3 import *

class CircuitBuilder():
    def build(self, nodes, outputs):
        circuit_outputs = []

        for output_name in outputs:
            circuit_outputs.append(self.__construct(nodes, output_name))

        return circuit_outputs

    def __construct(self, nodes, name):
        node = nodes[name]
        input_names = node.inputs

        if len(input_names) == 0:
            return Bool(name)

        input_logic = []
        for input_name in input_names:
            input_logic.append(self.__construct(nodes, input_name))

        if node.type == "And":
            return And(*input_logic)
        elif node.type == "Xor":
            return Xor(*input_logic)
        else:
            print("Unknown node type " + node.type)




from z3 import *
from tokenizer import Tokenizer
from parser import Parser
from circuit_builder import CircuitBuilder

class OracleRunner:
    def get_outputs(self, filename, inputs):
        with open(filename) as f:
            t = Tokenizer(f)
            p = Parser()

            nodes, outputs = p.parse(t)

            builder = CircuitBuilder()
            oracle = builder.build(nodes, outputs)

            s = Solver()
            input_objs = [Bool(i) for i in self.__primary_inputs(inputs)]

            for i in input_objs:
                s.add(i == inputs[i])

            outputs = [None] * len(oracle)
            for i in range(len(oracle)):
                s.push()
                s.add(oracle[i] == True)
                outputs[i] = str(s.check()) == "sat"
                s.pop()

            print("=== Oracle ===")
            print(oracle)
            print(outputs)
            return outputs

    def __primary_inputs(self, inputs):
        names = []

        for i in inputs:
            if not "key" in str(i):
                names.append(str(i))

        return names

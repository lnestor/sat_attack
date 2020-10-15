from z3 import *

from tokenizer import Tokenizer
from parser import Parser
from circuit_builder import CircuitBuilder

if __name__ == "__main__":
    with open("benchmarks/sample.v") as f:
        t = Tokenizer(f)
        p = Parser()
        nodes, outputs = p.parse(t)

        builder = CircuitBuilder()
        miter_circuit = builder.build_miter(nodes, outputs)

        s = Solver()
        s.add(miter_circuit == True)
        print(miter_circuit)
        print(s.check())
        print(s.model())

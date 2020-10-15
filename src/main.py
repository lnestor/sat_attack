from z3 import *

from tokenizer import Tokenizer
from parser import Parser
from circuit_builder import CircuitBuilder
from oracle_runner import OracleRunner

if __name__ == "__main__":
    with open("benchmarks/sample_multiple_outputs.v") as f:
        t = Tokenizer(f)
        p = Parser()
        nodes, outputs = p.parse(t)

        builder = CircuitBuilder()
        miter_circuit = builder.build_miter(nodes, outputs)

        s = Solver()
        s.add(miter_circuit == True)

        print("=== Model ===")
        print(miter_circuit)
        print(s.check())
        print(s.model())

        o = OracleRunner()
        oracle_outputs = o.get_outputs("benchmarks/sample_multiple_outputs_oracle.v", s.model())

        # Run against all keys

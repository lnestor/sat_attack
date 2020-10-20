from z3 import *

from circuit import Circuit
from circuit_solver import solve_ckt
from dip_finder import DipFinder
from key_space import KeySpace
from tokenizer import Tokenizer
from oracle_runner import OracleRunner
from parser import Parser

def read_bench_nodes(filename):
    """
    Reads in the nodes of a circuit from a benchmakr file.

    filename: the name of the benchmark file

    returns: the nodes of the circuit, the output names of the circuit
    """
    with open(filename) as f:
        t = Tokenizer(f)
        p = Parser()
        nodes, output_names = p.parse(t)
        return nodes, output_names

def read_bench_ckt(filename):
    """
    Reads in a circuit from a benchmark file.
    filename: the name of the benchmark file
    returns: object representation of the circuit
    """
    nodes, output_names = read_bench_nodes(filename)
    return Circuit.from_nodes(nodes, output_names)

if __name__ == "__main__":
    print("Reading in locked circuit...")
    # locked_nodes, locked_output_names = read_bench_nodes("benchmarks/sample/sample_locked.v")
    locked_nodes, locked_output_names = read_bench_nodes("benchmarks/c1335-RN320/c1355-RN320.v")
    finder = DipFinder(locked_nodes, locked_output_names)

    print("Reading in unlocked oracle...")
    # oracle_ckt = read_bench_ckt("benchmarks/sample/sample_unlocked.v")
    oracle_ckt = read_bench_ckt("benchmarks/c1335-RN320/c1355-oracle.v")
    runner = OracleRunner(oracle_ckt)

    dips = []
    oracle_outputs = []
    while finder.can_find_dip():
        print("=== ITERATION ===")
        dip = finder.find_dip()
        print("DIP: " + str(dip))

        oracle_output = runner.run(dip)
        print("ORACLE: " + str(oracle_output))

        finder.add_constraint(dip, oracle_output)

        dips.append(dip)
        oracle_outputs.append(oracle_output)

    s = Solver()
    for i in range(len(dips)):
        constraint_ckt = Circuit.specify_inputs(dips[i], locked_nodes, locked_output_names)

        output_constraints = []
        for name in constraint_ckt.outputs():
            output_constraints.append(constraint_ckt.outputs()[name] == oracle_outputs[i][name])

        s.add(*output_constraints)

    print(s.check())
    print(s.model())

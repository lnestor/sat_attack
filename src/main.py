from circuit import Circuit
from circuit_solver import solve_ckt
from dip_finder import DipFinder
from key_space import KeySpace
from tokenizer import Tokenizer
from oracle_runner import OracleRunner
from parser import Parser

def read_benchmark(filename):
    """
    Reads in a circuit from a benchmark file.

    filename: the name of the benchmark file

    returns: object representation of the circuit
    """
    with open(filename) as f:
        t = Tokenizer(f)
        p = Parser()
        nodes, output_names = p.parse(t)
        return Circuit(nodes, output_names)

def find_incorrect_keys(locked_ckt, key_space, oracle_output, dip):
    incorrect_keys = []

    for key_vector in key_space:
        locked_output = solve_ckt(locked_ckt, {**dip, **key_vector})

        if locked_output != oracle_output:
            incorrect_keys.append(key_vector)

    return incorrect_keys

if __name__ == "__main__":
    locked_ckt = read_benchmark("benchmarks/sample/sample_locked.v")
    # locked_ckt = read_benchmark("benchmarks/sample_multiple_outputs.v")
    key_space = KeySpace(locked_ckt)
    finder = DipFinder(locked_ckt)

    oracle_ckt = read_benchmark("benchmarks/sample/sample_unlocked.v")
    # oracle_ckt = read_benchmark("benchmarks/sample_multiple_outputs_oracle.v")
    runner = OracleRunner(oracle_ckt)

    while len(key_space) > 1:
        print("=== Iteration ===")
        dip = finder.find_dip()
        print("DIP: " + str(dip))

        oracle_output = runner.run(dip)
        print("Oracle: " + str(oracle_output))

        incorrect_keys = find_incorrect_keys(locked_ckt, key_space, oracle_output, dip)
        print("Incorrect keys: " + str(incorrect_keys))
        print("")

        if len(incorrect_keys) == 0:
            break

        key_space.remove(incorrect_keys)
        finder.mark_incorrect_keys(incorrect_keys)


    print("=== Remaining keys ===")
    for i in key_space:
        print(i)

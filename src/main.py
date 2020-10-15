from z3 import *

from tokenizer import Tokenizer
from parser import Parser
from circuit_builder import CircuitBuilder
from circuit_solver import solve_ckt

def extract_values_from_model(model, key_input_names, p_input_names):
    """
    Extracts the boolean values for each input from a given model from the z3 solver.
    The objects returned from solver.solve() are a special z3 format, so this function
    converts them into a more useable form.

    model: the model returned from a z3 solver
    key_input_names: the names of key inputs
    p_input_names: the names of primary inputs

    returns: values of key inputs, values of primary inputs
    """

    key_input_vals = []
    p_input_vals = []
    for i in model:
        if str(i) in key_input_names:
            key_input_vals.append(model[i])
        else:
            p_input_vals.append(model[i])

    return key_input_vals, p_input_vals

def read_benchmark(filename):
    """
    Reads in a circuit from a benchmark file.

    filename: the name of the benchmark file

    returns: nodes of circuit, name of output nodes
    """
    with open(filename) as f:
        t = Tokenizer(f)
        p = Parser()
        nodes, output_names = p.parse(t)
        return nodes, output_names

def run_oracle(filename, input_names, input_values):
    # TODO: this doesn't really need to be it's own function I think
    nodes, output_names = read_benchmark(filename)
    builder = CircuitBuilder()
    oracle_ckt, input_names, _ = builder.build(nodes, output_names)
    return solve_ckt(oracle_ckt, input_names, input_values)

def prune_keys(nodes, output_names, oracle_outputs, p_input_names, p_input_vals):
    locked_ckt, p_input_names, key_input_names = builder.build(nodes, output_names)

    for i in range(2**len(key_input_names)):
        key_input_values = [int(i / (2**name_index) % 2) == 0 for name_index, _ in enumerate(key_input_names)]
        locked_outputs = solve_ckt(locked_ckt, key_input_names + p_input_names, key_input_values + p_input_vals)

        if locked_outputs != oracle_outputs:
            print(locked_outputs)
            # These keys are incorrect, prune them


if __name__ == "__main__":
    nodes, output_names = read_benchmark("benchmarks/sample_multiple_outputs.v")

    builder = CircuitBuilder()
    miter_ckt, p_input_names, key_input_names = builder.build_miter(nodes, output_names)

    s = Solver()
    s.add(miter_ckt == True)
    s.check() # TODO: handle when this doesn't work

    key_input_vals, p_input_vals = extract_values_from_model(s.model(), key_input_names, p_input_names)

    oracle_outputs = run_oracle("benchmarks/sample_multiple_outputs_oracle.v", p_input_names, p_input_vals)
    print(oracle_outputs)

    prune_keys(nodes, output_names, oracle_outputs, p_input_names, p_input_vals)

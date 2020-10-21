import circuit
import tokenizer
import parser

def read_nodes(filename):
    """
    Reads in the nodes of a circuit from a benchmakr file.
    filename: the name of the benchmark file
    returns: the nodes of the circuit, the output names of the circuit
    """
    with open(filename) as f:
        t = tokenizer.Tokenizer(f)
        p = parser.Parser()
        nodes, output_names = p.parse(t)
        return nodes, output_names

def read_ckt(filename):
    """
    Reads in a circuit from a benchmark file.
    filename: the name of the benchmark file
    returns: object representation of the circuit
    """
    nodes, output_names = read_nodes(filename)
    return circuit.Circuit.from_nodes(nodes, output_names)

def get_expected_key(filename):
    key = {}

    with open(filename) as f:
        for line in f.readlines():
            if "KeyGate" in line:
                tokens = line.split()

                key_name = tokens[2][0:-1]
                key_bit = tokens[0] == "xnor"

                if "NOT" in tokens[1]:
                    key_bit = not key_bit

                key[key_name] = key_bit

    return key

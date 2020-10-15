from z3 import *

def solve_ckt(ckt, inputs):
    """
    Solves for the outputs of a circuit. This function requires that ALL inputs are
    passed in or else it is likely that the circuit outputs will all be True.
    """
    s = Solver()

    for name, value in inputs.items():
        input_obj = Bool(name)
        s.add(input_obj == value)

    z3_ckt = ckt.z3_repr()
    outputs = [None] * len(z3_ckt)
    for i in range(len(z3_ckt)):
        s.push()
        s.add(z3_ckt[i] == True)
        outputs[i] = str(s.check()) == "sat"
        s.pop()

    return outputs


def solve_ckt_old(ckt, input_names, input_values):
    """
    Solves for the outputs of a circuit. This function requires that ALL inputs are
    passed in or else it is likely that the circuit outputs will all be True.

    ckt: the z3 representation of the ckt
    input_names: the names of the input nodes
    input_values: the values for each input

    returns: the value for each output of the circuit
    """
    s = Solver()

    input_objs = [Bool(name) for name in input_names]
    for i in range(len(input_objs)):
        s.add(input_objs[i] == input_values[i])

    outputs = [None] * len(ckt)
    for i in range(len(ckt)):
        s.push()
        s.add(ckt[i] == True)
        outputs[i] = str(s.check()) == "sat"
        s.pop()

    return outputs


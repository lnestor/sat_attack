from z3 import *

def solve_ckt(ckt, inputs):
    """
    Solves for the outputs of a circuit. This function requires that ALL inputs are
    passed in or else it is likely that the circuit outputs will all be True.

    ckt: the circuit object
    inputs: the inputs to the circuit
    """
    s = Solver()

    for name, value in inputs.items():
        input_obj = Bool(name)
        s.add(input_obj == value)

    outputs = ckt.outputs()
    values = {}
    for name in outputs:
        s.push()
        s.add(outputs[name] == True)
        values[name] = str(s.check()) == "sat"
        s.pop()

    return values


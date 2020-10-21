from circuit_builder import CircuitBuilder

class Circuit:
    @classmethod
    def miter(cls, ckt0, ckt1):
        """
        Creates a miter circuit given two input circuits. The outputs
        of the input circuits will be XORed and the ORed into a diff signal.

        ckt0: Circuit object representing the first half of the miter circuit
        ckt1: Circuit object representing the second half of the miter circuit
        returns: Circuit object representing the miter circuit
        """
        builder = CircuitBuilder()
        miter_ckt = builder.build_miter(ckt0, ckt1)
        return cls(miter_ckt, ckt0.primary_inputs())

    @classmethod
    def from_nodes(cls, nodes, output_names, key_suffix = ""):
        """
        Creates a circuit given a list of nodes read in from an input file.

        nodes: the nodes of the circuit
        output_names: the names of which nodes are outputs
        key_suffix: an optional suffix to apply to all key inputs in the circuit
        returns: Circuit object corresponding to nodes given
        """
        builder = CircuitBuilder()
        z3_ckt, inputs = builder.build(nodes, output_names, key_suffix)
        return cls(z3_ckt, inputs)

    @classmethod
    def specify_inputs(cls, inputs, nodes, output_names, key_suffix = ""):
        """
        Creates a circuit given nodes. It also replaces input nodes with
        values specified.

        inputs: the inputs to replace in the circuit
        nodes: the nodes of the circuit
        output_names: the names of which nodes are outputs
        key_suffix: an optional suffix to apply to all key inputs in the circuit
        returns: Circuit object corresponding to nodes given with inputs replaced
        """
        builder = CircuitBuilder()
        z3_ckt, inputs = builder.build(nodes, output_names, key_suffix, inputs)
        return cls(z3_ckt, inputs)

    def __init__(self, z3_ckt, inputs):
        self.z3_ckt = z3_ckt
        self.inputs = inputs
        self._primary_inputs = None
        self._key_inputs = None

    def outputs(self):
        """Returns the z3 representation of the outputs of the circuit"""
        return self.z3_ckt

    def primary_inputs(self):
        """Returns the names of the primary inputs to the circuit"""
        if self._primary_inputs is not None:
            return self._primary_inputs
        else:
            self._primary_inputs = list(filter(lambda x: "key" not in x, self.inputs))
            return self._primary_inputs

    def key_inputs(self):
        """Returns the names of the key inputs to the circuit"""
        if self._key_inputs is not None:
            return self._key_inputs
        else:
            self._key_inputs = list(filter(lambda x: "key" in x, self.inputs))
            return self._key_inputs



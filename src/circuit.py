from circuit_builder import CircuitBuilder

class Circuit:
    def __init__(self, nodes, output_names):
        self._nodes = nodes
        self._outputs = output_names

        builder = CircuitBuilder()
        self._miter_ckt, self._primary_inputs, self._miter_key_inputs = builder.build_miter(self._nodes, self._outputs)
        self._ckt, _, self._key_inputs = builder.build(self._nodes, self._outputs)

    def z3_miter(self):
        """Returns the z3 representation of a miter circuit."""
        return self._miter_ckt

    def z3_repr(self):
        """Returns the z3 representation of a single circuit."""
        return self._ckt

    def primary_inputs(self):
        return self._primary_inputs

    def key_inputs(self):
        return self._key_inputs

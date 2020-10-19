from circuit_builder import CircuitBuilder

class Circuit:
    @classmethod
    def miter(cls, ckt0, ckt1):
        builder = CircuitBuilder()
        miter_ckt = builder.build_miter(ckt0, ckt1)
        return cls(miter_ckt, ckt0.primary_inputs())

    @classmethod
    def from_nodes(cls, nodes, output_names, key_suffix = ""):
        builder = CircuitBuilder()
        z3_ckt, inputs = builder.build(nodes, output_names, key_suffix)
        return cls(z3_ckt, inputs)

    @classmethod
    def specify_inputs(cls, inputs, nodes, output_names, key_suffix = ""):
        builder = CircuitBuilder()
        z3_ckt, _ = builder.build(nodes, output_names, key_suffix, inputs)
        return cls(z3_ckt, inputs.keys())

    def __init__(self, z3_ckt, inputs):
        self.z3_ckt = z3_ckt
        self.inputs = inputs
        self._primary_inputs = None

    def outputs(self):
        return self.z3_ckt

    def primary_inputs(self):
        if self._primary_inputs is not None:
            return self._primary_inputs
        else:
            # find primary inputs
            self._primary_inputs = list(filter(lambda x: "key" not in x, self.inputs))
            return self._primary_inputs




class CircuitOld:
    def __init__(self, nodes, output_names):
        self._nodes = nodes
        self._outputs = output_names

        builder = CircuitBuilder()
        self._miter_ckt, self._primary_inputs, self._miter_key_inputs = builder.build_miter(self._nodes, self._outputs)
        self._ckt, _, self._key_inputs = builder.build(self._nodes, self._outputs)

        self._miter_ckt_part0, _, _ = builder.build(self._nodes, self._outputs, "ckt0")
        self._miter_ckt_part1, _, _ = builder.build(self._nodes, self._outputs, "ckt1")

    def z3_miter(self):
        """Returns the z3 representation of a miter circuit."""
        return self._miter_ckt

    def z3_repr(self):
        """Returns the z3 representation of a single circuit."""
        return self._ckt

    def z3_miter_parts(self):
        return self._miter_ckt_part0, self._miter_ckt_part1

    def primary_inputs(self):
        return self._primary_inputs

    def key_inputs(self):
        return self._key_inputs

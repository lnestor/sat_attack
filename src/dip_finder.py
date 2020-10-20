from z3 import *
from circuit import Circuit

class DipFinder:
    def __init__(self, nodes, output_names):
        self.nodes = nodes
        self.output_names = output_names

        self.locked_ckt0 = Circuit.from_nodes(nodes, output_names, key_suffix = "__ckt0")
        self.locked_ckt1 = Circuit.from_nodes(nodes, output_names, key_suffix = "__ckt1")
        self.miter_ckt = Circuit.miter(self.locked_ckt0, self.locked_ckt1)

        self.solver = Solver()
        self.solver.add(self.miter_ckt.outputs()["diff"] == True)

    def can_find_dip(self):
        return self.solver.check() == sat

    def find_dip(self):
        model = self.solver.model()
        return self._extract_dip_from_model(model)

    def add_constraint(self, dip, outputs):
        constraint_ckt0 = Circuit.specify_inputs(dip, self.nodes, self.output_names, key_suffix = "__ckt0")
        constraint_ckt1 = Circuit.specify_inputs(dip, self.nodes, self.output_names, key_suffix = "__ckt1")

        output_constraints0 = []
        output_constraints1 = []

        for name in constraint_ckt0.outputs():
            output_constraints0.append(constraint_ckt0.outputs()[name] == outputs[name])
            output_constraints1.append(constraint_ckt1.outputs()[name] == outputs[name])

        self.solver.add(*output_constraints0)
        self.solver.add(*output_constraints1)

    def _extract_dip_from_model(self, model):
        primary_inputs = self.miter_ckt.primary_inputs()
        dip = {}

        for input in model:
            if str(input) in primary_inputs:
                dip[str(input)] = model[input]

        remaining_inputs = [x for x in primary_inputs if x not in dip.keys()]
        for input in remaining_inputs:
            dip[input] = False


        return dip

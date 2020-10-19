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

        for p_input in primary_inputs:
            for input in model:
                if str(input) in primary_inputs:
                    dip[p_input] = model[input]
                else:
                    dip[p_input] = False
        # for input in model:
        #     if str(input) in primary_inputs:
        #         dip[str(input)] = model[input]

        return dip

# class DipFinderOld:
#     def __init__(self, ckt):
#         self.ckt = ckt
#         self.solver = Solver()
#         self.solver.add(ckt.z3_miter() == True)

#     def find_dip(self):
#         if str(self.solver.check()) != "sat":
#             print("No dip found")
#             return None

#         model = self.solver.model()
#         return self.__extract_dip_from_model(model)

#     def add_constraint(self, inputs, outputs):
#         input_constraints = []
#         for name, value in inputs.items():
#             z3obj = Bool(name)
#             input_constraints.append(z3obj == value)

#         miter_part0, miter_part1 = self.ckt.z3_miter_parts()

#         output_constraints0 = []
#         output_constraints1 = []
#         for i in range(len(outputs)):
#             output_constraints0.append(miter_part0[i] == outputs[i])
#             output_constraints1.append(miter_part1[i] == outputs[i])

#         self.solver.add(Implies(And(*input_constraints), And(*output_constraints0)))
#         self.solver.add(Implies(And(*input_constraints), And(*output_constraints1)))

#     def mark_incorrect_keys(self, keys):
#         for key in keys:
#             self.mark_incorrect_key_single(key)

#     def mark_incorrect_key_single(self, key):
#         # TODO: redo this better
#         key_constraints_ckt0 = []
#         key_constraints_ckt1 = []
#         for name, value in key.items():
#             z3obj0 = Bool(name + "__ckt0")
#             z3obj1 = Bool(name + "__ckt1")
#             key_constraints_ckt0.append(z3obj0 == value)
#             key_constraints_ckt1.append(z3obj1 == value)

#         self.solver.add(And(*key_constraints_ckt0) == False)
#         self.solver.add(And(*key_constraints_ckt1) == False)

#     def __extract_dip_from_model(self, model):
#         primary_inputs = self.ckt.primary_inputs()
#         dip = {}

#         for input in model:
#             if str(input) in primary_inputs:
#                 dip[str(input)] = model[input]

#         return dip


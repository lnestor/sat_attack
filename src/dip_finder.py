from z3 import *

class DipFinder:
    def __init__(self, ckt):
        self.ckt = ckt
        self.solver = Solver()
        self.solver.add(ckt.z3_miter() == True)

    def find_dip(self):
        self.solver.check()
        model = self.solver.model()

        return self.__extract_dip_from_model(model)

    def mark_incorrect_keys(self, keys):
        for key in keys:
            self.mark_incorrect_key_single(key)

    def mark_incorrect_key_single(self, key):
        key_constraints = []
        for name, value in key.items():
            z3obj = Bool(name)
            key_constraints.append(z3obj == value)

        self.solver.add(And(*key_constraints) == False)

    def __extract_dip_from_model(self, model):
        primary_inputs = self.ckt.primary_inputs()
        dip = {}

        for input in model:
            if str(input) in primary_inputs:
                dip[str(input)] = model[input]

        return dip


from z3 import *

class DipFinder:
    def __init__(self, ckt):
        self.ckt = ckt
        self.solver = Solver()
        self.solver.add(ckt.z3_miter() == True)

    def find_dip(self):
        if str(self.solver.check()) != "sat":
            print("ERROR - not satisfied")
            raise

        model = self.solver.model()
        return self.__extract_dip_from_model(model)

    def mark_incorrect_keys(self, keys):
        for key in keys:
            self.mark_incorrect_key_single(key)

    def mark_incorrect_key_single(self, key):
        # TODO: redo this better
        key_constraints_ckt0 = []
        key_constraints_ckt1 = []
        for name, value in key.items():
            z3obj0 = Bool(name + "__ckt0")
            z3obj1 = Bool(name + "__ckt1")
            key_constraints_ckt0.append(z3obj0 == value)
            key_constraints_ckt1.append(z3obj1 == value)

        self.solver.add(And(*key_constraints_ckt0) == False)
        self.solver.add(And(*key_constraints_ckt1) == False)

    def __extract_dip_from_model(self, model):
        primary_inputs = self.ckt.primary_inputs()
        dip = {}

        for input in model:
            if str(input) in primary_inputs:
                dip[str(input)] = model[input]

        return dip


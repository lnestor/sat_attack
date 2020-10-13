from z3 import *

class Parser():
    def __init__(self):
        self.nodes = {}

    def parse(self, fobj):
        for line in fobj.readlines():
            tokens = line.split(" ")

            if tokens[0] == "input":
                self.add_bools(tokens[1:])
            # elif tokens[0] == "output":
            # elif tokens[0] == "and":
            # elif tokens[0] == "xor":
            else:
                print("Skipping line " + str(tokens))

    def add_bools(self, names):
        for name in names:
            self.nodes[name] = Bool(name)

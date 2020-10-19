class Node():
    def __init__(self, name, inputs, type):
        self.name = name
        self.inputs = inputs
        self.type = type
        self.z3_repr = None

    def __str__(self):
        return "<" + str(self.name) + ": " + str(self.type) + " " + str(self.inputs) + ">"

    def __repr__(self):
        return "<" + str(self.name) + ": " + str(self.type) + " " + str(self.inputs) + ">"

from z3 import *

from circuit import Circuit
import sat_model

class DipFinder:
    def __init__(self, nodes, output_names):
        self.nodes = nodes
        self.output_names = output_names
    # def __init__(self, ckt_graph):
    #     self.ckt_graph = ckt_graph

    #     self.locked_ckt0 = Circuit.from_nodes(self.ckt_graph.nodes, self.ckt_graph.outputs, key_suffix = "__ckt0")
    #     self.locked_ckt1 = Circuit.from_nodes(self.ckt_graph.nodes, self.ckt_graph.outputs, key_suffix = "__ckt1")
        self.locked_ckt0 = Circuit.from_nodes(nodes, output_names, key_suffix = "__ckt0")
        self.locked_ckt1 = Circuit.from_nodes(nodes, output_names, key_suffix = "__ckt1")
        self.miter_ckt = Circuit.miter(self.locked_ckt0, self.locked_ckt1)

        self.solver = Solver()
        self.goal = Goal()
        self.solver.add(self.miter_ckt.outputs()["diff"] == True)
        self.goal.add(self.miter_ckt.outputs()["diff"] == True)
        self.metrics()

    def can_find_dip(self):
        """Returns if a dip can be found given the current constraints"""
        return self.solver.check() == sat

    def find_dip(self):
        """Returns a dip for the circuit given the current constraints"""
        model = self.solver.model()
        primary_inputs = self.miter_ckt.primary_inputs()
        return sat_model.extract_from_model(model, primary_inputs, completion=True)

    def add_constraint(self, dip, outputs):
        """
        Adds a new dip/output constraint to the SAT solver.

        dip: the DIP for the constraint
        outputs: the oracle outputs for the DIP passed in
        """
        constraint_ckt0 = Circuit.specify_inputs(dip, self.nodes, self.output_names, key_suffix = "__ckt0")
        constraint_ckt1 = Circuit.specify_inputs(dip, self.nodes, self.output_names, key_suffix = "__ckt1")

        output_constraints0 = []
        output_constraints1 = []

        for name in constraint_ckt0.outputs():
            output_constraints0.append(constraint_ckt0.outputs()[name] == outputs[name])
            output_constraints1.append(constraint_ckt1.outputs()[name] == outputs[name])

        self.solver.add(*output_constraints0)
        self.solver.add(*output_constraints1)
        self.goal.add(*output_constraints0)
        self.goal.add(*output_constraints1)

        self.metrics()

    def metrics(self):
        num_clauses = []
        num_variables = []

        # print("Converting to tseitin-cnf")
        tactic = z3.Tactic("tseitin-cnf")
        cnf = tactic(self.goal)[0]

        variables = set()
        for clause in cnf:
            if len(clause.children()) == 0:
                input_name = str(clause)
                variables.add(input_name)

            for child in clause.children():
                if len(child.children()) == 0:
                    input_name = str(child)
                    variables.add(input_name)
                elif len(child.children()) == 1:
                    input_name = str(child.children()[0])
                    variables.add(input_name)
                else:
                    print("More than one child present (%i)" % (len(child.children)))

        if len(cnf) != 0:
            num_clauses.append(len(cnf))

        num_variables.append(len(variables))

        print("%i,%i" % (num_clauses[0], num_variables[0]))

        # print("\nNumber of clauses: " + repr(num_clauses))
        # print("Average number of clauses: " + str(sum(num_clauses) / len(num_clauses)))
        # print("Max number of clauses: " + str(max(num_clauses)))
        # print("Average number of variables: " + str(sum(num_variables) / len(num_variables)))
        # print("Max number of variables: " + str(max(num_variables)))

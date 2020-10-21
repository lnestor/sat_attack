from circuit_solver import solve_ckt

class OracleRunner:
    def __init__(self, ckt):
        self.ckt = ckt

    def run(self, inputs):
        """Run a set of inputs against the oracle"""
        return solve_ckt(self.ckt, inputs)

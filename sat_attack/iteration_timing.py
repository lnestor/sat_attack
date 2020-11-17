import time

class IterationTiming:
    """Data class to hold timing information for a single iteration of a SAT attack.

    Each iteration is time in the following criteria:
     - Total time
     - Time SAT solving
     - Time overhead

    """
    def __init__(self):
        self.start_time = time.time()

    def start_sat(self):
        self.sat_start = time.time()

    def end_sat(self):
        self.sat_time = time.time() - self.sat_start

    def start_oracle(self):
        self.oracle_start = time.time()

    def end_oracle(self):
        self.oracle_time = time.time() - self.oracle_start

    def start_constraint(self):
        self.constraint_start = time.time()

    def end_constraint(self):
        self.constraint_time = time.time() - self.constraint_start

    def end_iteration(self):
        self.total_time = time.time() - self.start_time

    def print(self, iteration):
        print("Iteration %i:" % (iteration))
        print("  Total Time: %f" % (self.total_time))
        print("  Time SAT solving: %f" % (self.sat_time))
        print("  Time running DIP on oracle: %f" % (self.oracle_time))
        print("  Time adding new constraint: %f\n" % (self.constraint_time))

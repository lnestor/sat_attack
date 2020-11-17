import statistics
import time
import z3

import benchmarks
import circuit
import dip_finder
import iteration_timing
import sat_model
import oracle_runner

class SatAttack:
    """The main class for conducting the SAT attack."""

    def __init__(self, locked_filename, unlocked_filename):
        self.locked_filename = locked_filename
        self.unlocked_filename = unlocked_filename
        self.iterations = 0

    def run(self, timeout, detailed):
        """Run the SAT attack."""

        start_time = time.time()
        timed_out = False

        print("Reading in locked circuit...")
        self.nodes, self.output_names = benchmarks.read_nodes(self.locked_filename)

        print("Reading in unlocked circuit...")
        self.oracle_ckt = benchmarks.read_ckt(self.unlocked_filename)

        key_inputs = [node.name for node in self.nodes.values() if node.type == "Key Input"]
        primary_inputs = [node.name for node in self.nodes.values() if node.type == "Primary Input"]

        print("\n# Primary Inputs: %i" % (len(primary_inputs)))
        print("# Key Inputs: %i\n" % (len(key_inputs)))

        finder = dip_finder.DipFinder(self.nodes, self.output_names)
        runner = oracle_runner.OracleRunner(self.oracle_ckt)

        oracle_io_pairs = []
        timings = []
        while finder.can_find_dip():
            timing = iteration_timing.IterationTiming()
            timings.append(timing)

            timing.start_sat()
            dip = finder.find_dip()
            timing.end_sat()

            timing.start_oracle()
            oracle_output = runner.run(dip)
            timing.end_oracle()

            timing.start_constraint()
            finder.add_constraint(dip, oracle_output)
            timing.end_constraint()

            timing.end_iteration()
            oracle_io_pairs.append((dip, oracle_output))
            self.iterations += 1

            if detailed:
                timing.print(self.iterations)

            if timeout is not None and time.time() - start_time > timeout:
                timed_out = True
                break

        if timed_out:
            print("\nSAT attack ran too long... timed out")
            print("Timeout was %is, ran for %fs\n" % (timeout, time.time() - start_time))

        iteration_times = [t.total_time for t in timings]
        print("# Iterations: %i" % (self.iterations))
        print("Average time/iteration: %f" % (sum(iteration_times) / len(iteration_times)))
        print("Stdev of time/iteration: %f" % (statistics.stdev(iteration_times)))

        print("\nFinding key...")
        key = self._find_key(oracle_io_pairs, key_inputs)
        expected_key = benchmarks.get_expected_key(self.locked_filename)

        print("\nExpected key: %s" % (self._key_string(expected_key)))
        print("Found key:    %s" % (self._key_string(key)))

        print("\nChecking for circuit equivalence...")
        self._check_key(key)
        if self._check_key(key):
            print("Locked and unlocked circuits match\n")
        else:
            print("Key found does not match oracle\n")

    def _find_key(self, oracle_io_pairs, key_names):
        """
        Find a key that satisfies all DIPs found during the SAT attack.
        This key will be in the set of correct keys.

        oracle_io_pairs: array of dip/output pairs in the form of (dip, output)

        returns: key that satisfies all dip constraints
        """

        s = z3.Solver()

        for io_pair in oracle_io_pairs:
            dip = io_pair[0]
            output = io_pair[1]

            constraint_ckt = circuit.Circuit.specify_inputs(dip, self.nodes, self.output_names)
            output_constraints = [constraint_ckt.outputs()[name] == output[name] for name in output.keys()]

            s.add(*output_constraints)

        s.check()
        model = s.model()
        key = sat_model.extract_from_model(model, key_names, completion=True)
        return key

    def _check_key(self, key):
        """
        Check that the key returned from the SAT attack is correct. It
        does this by creating a miter circuit with a locked version
        and an oracle. If the diff signal returned from the miter circuit
        cannot be True, then the circuits are equivalent.

        key: the key returned from the SAT attaack
        """

        locked_ckt = circuit.Circuit.specify_inputs(key, self.nodes, self.output_names)
        miter = circuit.Circuit.miter(locked_ckt, self.oracle_ckt)

        s = z3.Solver()
        s.add(miter.outputs()["diff"] == True)

        return s.check() == z3.unsat

    def _key_string(self, key):
        ordered_names = sorted(key.keys(), key=lambda name: int(name[8:]))
        key_string = ""

        for name in ordered_names:
            if key[name]:
                key_string += "1"
            else:
                key_string += "0"

        return key_string





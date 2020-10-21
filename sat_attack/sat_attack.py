import z3

import benchmarks
import circuit
import dip_finder
import sat_model
import oracle_runner

class SatAttack:
    """The main class for conducting the SAT attack."""

    def __init__(self, locked_filename, unlocked_filename):
        self.locked_filename = locked_filename
        self.unlocked_filename = unlocked_filename
        self.iterations = 0

    def run(self):
        """Run the SAT attack."""
        print("Reading in locked circuit...")
        self.nodes, self.output_names = benchmarks.read_nodes(self.locked_filename)

        print("Reading in unlocked circuit...")
        self.oracle_ckt = benchmarks.read_ckt(self.unlocked_filename)

        finder = dip_finder.DipFinder(self.nodes, self.output_names)
        runner = oracle_runner.OracleRunner(self.oracle_ckt)

        oracle_io_pairs = []
        while finder.can_find_dip():
            dip = finder.find_dip()
            oracle_output = runner.run(dip)
            finder.add_constraint(dip, oracle_output)

            oracle_io_pairs.append((dip, oracle_output))
            self.iterations += 1

        key = self._find_key(oracle_io_pairs)
        self._check_key(key)

    def _find_key(self, oracle_io_pairs):
        """
        Find a key that satisfies all DIPs found during the SAT attack.
        This key will be in the set of correct keys.

        oracle_io_pairs: array of dip/output pairs in the form of (dip, output)

        returns: key that satisfies all dip constraints
        """

        s = z3.Solver()
        key_names = None

        for io_pair in oracle_io_pairs:
            dip = io_pair[0]
            output = io_pair[1]

            constraint_ckt = circuit.Circuit.specify_inputs(dip, self.nodes, self.output_names)
            output_constraints = [constraint_ckt.outputs()[name] == output[name] for name in output.keys()]

            s.add(*output_constraints)

            if key_names == None:
                key_names = constraint_ckt.key_inputs()

        s.check()
        model = s.model()
        key = sat_model.extract_from_model(model, key_names)
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

        if s.check() == z3.sat:
            print("Key found does not match oracle")
        else:
            print("Locked and unlocked circuits match")


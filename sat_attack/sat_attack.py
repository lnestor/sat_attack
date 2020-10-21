import z3

import benchmarks
import circuit
import dip_finder
import sat_model
import oracle_runner

class SatAttack:
    def __init__(self, locked_filename, unlocked_filename):
        self.locked_filename = locked_filename
        self.unlocked_filename = unlocked_filename

    def run(self):
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

        key = self.find_key(oracle_io_pairs)
        self.check_key(key)

    def find_key(self, oracle_io_pairs):
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

    def check_key(self, key):
        locked_ckt = circuit.Circuit.specify_inputs(key, self.nodes, self.output_names)
        miter = circuit.Circuit.miter(locked_ckt, self.oracle_ckt)

        s = z3.Solver()
        s.add(miter.outputs()["diff"] == True)

        if s.check() == z3.sat:
            print("Key found does not match oracle")
        else:
            print("Locked and unlocked circuits match")


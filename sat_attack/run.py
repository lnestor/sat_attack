import argparse
import time

import sat_attack

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform a SAT attack on a locked circuit.")
    parser.add_argument("locked_ckt", help="The locked benchmark file")
    parser.add_argument("oracle", help="The unlocked benchmark file")

    args = parser.parse_args()

    attack = sat_attack.SatAttack(args.locked_ckt, args.oracle)

    start = time.time()
    attack.run()
    end = time.time()

    print("\nIterations: %i" % (attack.iterations))
    print("Elapsed time: %.3fs" % (end - start))


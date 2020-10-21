# A Poor Person's SAT Attack

This repository contains a basic implementation of the SAT attack described in [this paper](http://www.eecs.umich.edu/courses/eecs578/eecs578.f15/papers/sub15.pdf).

## Installation

[Python](https://www.python.org) is required to run this SAT attack.

Install all dependencies using the package manager [pip](https://pip.pypa.io/en/stable/).

```
pip install -r requirements.txt
```

## Usage

```
python3 sat_attack/run.py <LOCKED-FILE> <UNLOCKED-FILE>
```

## Description

A SAT attack is an oracle-guided attack on a logic locked circuit. Two copies of the locked circuit
are used, each having different key inputs but the same priamry inputs. A SAT solver is used
to determine a primary input such that the outputs of the two circuits will be different.
This output is called a distinguishing I/O pair (DIP).

The DIP is then applied to the oracle to figure out what the output should be. This IO pair
(DIP and oracle output) is then added as another clause to the SAT solver, ensuring that
the output of the circuit given that input and a key MUST be the oracle output. This
forces the SAT solver to never consider keys that are known to be incorrect.

The above process is done iteratively until a DIP can no longer be found. Then, a SAT solver
is used again with all the DIPs found. Any key which satisfies all DIP/oracle output pairs
is in the correct key class.

## Project Structure

A description of the project structure and what each file contains is below.

* `benchmarks.py`: contains helper functions for reading in benchmark files
* `circuit.py`: class representing a single circuit
* `circuit_builder.py`: helper class to convert from a node tree to a z3 representation of a circuit
* `circuit_solver.py`: contains a helper function to solve for circuit outputs given inputs
* `dip_finder.py`: class containing the SAT solver to find DIPs
* `node.py`: class representing an abstract node in the parsing process
* `oracle_runner`: helper class to run DIPs on an oracle
* `parser.py`: class to convert a stream of input tokens into a node tree
* `run.py`: entry point for the applications
* `sat_attack.py`: class that runs the actually SAT attack
* `sat_model.py`: contains a helper function to extract python literal values (True, False) from a z3 model
* `token_type.py`: enum to aid in the parser creating a node tree
* `tokenizer.py`: converts an input file to a stream of tokens, which are easier to deal with than text

## Relevant Papers

* [Evaluating the Security of Logic Encryption Algorithms](http://www.eecs.umich.edu/courses/eecs578/eecs578.f15/papers/sub15.pdf)
* [Keynote: A Disquisition on Logic Locking](https://par.nsf.gov/servlets/purl/10138106)
* [Anti-SAT: Mitigating SAT Attack on Logic Locking](https://eprint.iacr.org/2017/761.pdf)

## Future Improvements

* Add automated tests
* Add more benchmarks and support features necessary
* Support multiple Verilog modules because Anti-SAT benchmarks uses them

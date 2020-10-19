# To Work On

 - Add different gates
 - Add multi input gates (if needed)
 - Add command line arguments
 - Tests: add automated tests - lol
 - Figure out faster way to create the circuits
  - Multiple threads?
  - We recurse twice to create the miter circuit, we could probably just do it once
  - I think we may be evaluating a node several times if it is used several times. We should only be evaluating a node once and caching it
 - Iterating over the entire keyspace is extremely long for 32 key inputs (and that is the smallest available)
  - Should we prune a single key at a time?
  - Does z3 have any special features where we can figure out which keys give the incorrect response for a specified response?
  - I think we just add clauses to the solver that say "for this input, the output must be this" and then it won't ever suggest keys that don't satisfy that clause

```
sat_constraints = miter_circuit(I, K1, K2) == True
while satisfyable(sat_constraints):
  dip = extract_model(sat_constraints)
  outputs = oracle(dip)
  sat_constraints += circuit(dip, K1) == outputs
  sat_constraints += circuit(dip, K2) == outputs
```

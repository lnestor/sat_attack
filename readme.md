# To Work On

 - Add different gates
 - Add multi input gates (if needed)
 - Add command line arguments
 - Tests: add automated tests - lol
 - Iterating over the entire keyspace is extremely long for 32 key inputs (and that is the smallest available)
  - Should we prune a single key at a time?
  - Does z3 have any special features where we can figure out which keys give the incorrect response for a specified response?
  - I think we just add clauses to the solver that say "for this input, the output must be this" and then it won't ever suggest keys that don't satisfy that clause

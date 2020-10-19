from z3 import *

a = Bool("A")
b = Bool("B")
key = Bool("key")
ckt = Xor(key, And(a, b))

# con = (Implies(And(a == True, b == True), ckt == False))
con = (Implies(ckt == False, And(a == True, b == True)))
s = Solver()
s.add(con)

print(s.check())
print(s.model())

def f(x):
    yield x

# def f(x, y, z):
#     return Xor(z, And(x, y))


# s3 = Solver()
# s3.add(f(True, True, Bool("key")) == False)
# print(s3.check())
# print(s3.model())

# Could make the circuit a function that takes as inputs the keys and inputs
# and then pass in bools OR the IO pairs
# s2 = Solver()
# ckt2 = Xor(key, And(True, True))
# s2.add(ckt2 == False)
# print(s2.check())
# print(s2.model())


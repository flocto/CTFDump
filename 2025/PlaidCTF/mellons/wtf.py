from z3 import *

test = 0b10100011
x = BitVec('x', 8)
s = Solver()
s.add(x == test)

if s.check() == sat:
    m = s.model()
    print(bin(m.eval(Extract(7, 1, x)).as_long()))
    print(bin(m.eval(Extract(0, 0, x)).as_long()))
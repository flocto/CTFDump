from cvc5.pythonic import *

a = 2760624790958533
c = 4164880461924199
m = 4503599627370496
low = int(m/10*9)

x = BitVec('x', 64)
_x = x

s = Solver()

s.add(x > low)
s.add(x <= m)

for i in range(5):
    s.add(((a * _x + c) & (m - 1)) > low)
    _x = (a * _x + c) & (m - 1)
# s.add(((a * x + c) & (m - 1)) > x)

print(x)
while s.check() == sat:
    m = s.model()
    print(m, m[x])
    s.add(x != m[x].as_long())
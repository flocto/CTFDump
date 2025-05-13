import json
from z3 import *

code = open('index.html').readlines()
code = [line.strip() for line in code[34:145]]
attrs = json.loads(open('attrs.json').read())

s = Solver()
n = 30
flag = [BitVec(f'flag_{i}', 32) for i in range(n)]
stack = [f for f in flag]

for i in range(n):
    s.add(flag[i] >= 0x20)
    s.add(flag[i] <= 0x7e)

for line in code:
    parts = line.split('.')[1:]  # first one doesnt matter
    for part in parts:
        if part not in attrs:
            stack.append(BitVecVal(len(part) % 16, 32))
        else:
            match attrs[part]:
                case 0:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
                case 1:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
                case 2:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a * b)
                case 3:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b % a)
                case 4:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a ^ b)
                case 5:
                    stack.pop()
                case 6:
                    a = stack.pop()
                    a = simplify(a)
                    # print(a)
                    stack.append(stack[a.as_long()])
                case 7:
                    a = stack.pop()
                    b = stack.pop()
                    lhs = simplify(a)
                    rhs = simplify(b)
                    stack.append(
                        If(lhs == rhs, BitVecVal(1, 32), BitVecVal(0, 32)))
                case 8:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(simplify(a & b))
                case 9:
                    stack.pop(0)
                case _:
                    print('wtfs')


last = stack[-1]
s.add(last == 1)

if s.check() == sat:
    m = s.model()
    # print(m)
    flag = [m[f].as_long() for f in flag]
    flag = ''.join([chr(f) for f in flag])
    print(flag)
else:
    print('unsat')

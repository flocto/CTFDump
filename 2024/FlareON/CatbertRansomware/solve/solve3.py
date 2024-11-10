import z3
z3.set_option('parallel.enable', True)
# import cvc5.pythonic as z3

def ror32(x, n):
    return z3.RotateRight(x, n)

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(0x10)]
s = z3.Solver()
for i in range(0x10):
    # s.add(flag[i] >= 0x20, flag[i] <= 0x7e)
    # a-zA-Z0-9
    s.add(z3.Or(z3.And(flag[i] >= 0x30, flag[i] <= 0x39), z3.And(flag[i] >= 0x41, flag[i] <= 0x5a), z3.And(flag[i] >= 0x61, flag[i] <= 0x7a)))

known = b'VerYDumB'
for i in range(len(known)):
    s.add(flag[i] == known[i])

state = 0x1505
state = z3.BitVecVal(state, 32)

for i in range(4):
    inp = z3.ZeroExt(24, flag[i])
    state = (state << 5) + state + inp

s.add(state & 0xffffffff == 0x7c8df4cb)

state = z3.BitVecVal(0, 32)
for i in range(4, 8):
    inp = z3.ZeroExt(24, flag[i])
    state = ror32(state, 0xd)
    state += inp

s.add(state & 0xffffffff == 0x8b681d82)

A = z3.BitVecVal(1, 32)
B = z3.BitVecVal(0, 32)
for i in range(8, 16):
    inp = z3.ZeroExt(24, flag[i])
    A = (A + inp) % 0xfff1
    B = (B + A) % 0xfff1

# match3 = 0x0f910374
s.add(z3.And(B == 0x0f91, A == 0x0374))

C = 0x01000193
state = 0x811c9dc5
for i in range(8):
    # inp = z3.ZeroExt(24, flag[i])
    inp = known[i]
    state *= C
    # state %= 1 << 20
    state &= (1 << 32) - 1
    state ^= inp

# print(hex(state))

C = z3.BitVecVal(C, 32)
state = z3.BitVecVal(state, 32)

for i in range(8, 16):
    inp = z3.ZeroExt(24, flag[i])
    state *= C
    state &= (1 << 32) - 1
    state ^= inp

s.add(state == 0x31f009d2)

if s.check() == z3.sat:
    m = s.model()
    print(''.join(chr(m[flag[i]].as_long()) for i in range(16)))
    while s.check() == z3.sat:
        m = s.model()
        s.add(z3.Or([flag[i] != m[flag[i]] for i in range(16)]))
        print(''.join(chr(m[flag[i]].as_long()) for i in range(16)))

        # after a long time -> VerYDumBpassword
else:
    print('unsat')
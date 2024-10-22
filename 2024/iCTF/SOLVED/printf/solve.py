from dump import parse
# from z3 import *
from cvc5.pythonic import *
data = open('printf_patched', 'rb').read()

start = 0x2008
length = 0x168a2
data = data[start:start+length].decode()

insts = parse(data)

regs = [0, 0, 0, 0, 0, 0, 0, 0]
stack = []
flag = [BitVec(f'flag_{i}', 64) for i in range(72)]
flag_out = [0 for i in range(72)]
flag_i = 0

s = Solver()
for f in flag:
    s.add(f >= 0x20, f <= 0x7e)

def run(op, arg):
    global regs, stack, flag, flag_i, s
    if op == 'read':
        print('READ DETECTED') 
        # stack.append(ord(input()[0]))
        stack.append(flag[flag_i])
        flag_i += 1
    elif op == 'print':
        # print('PRINT DETECTED')
        print(chr(regs[0] & 0xff), end='')
    elif op == 'pop':
        regs[arg] = stack.pop()
    elif op == 'push_const':
        stack.append(arg)
    elif op == 'push_reg':
        stack.append(regs[arg])
    elif op == 'add':
        regs[arg] = stack[-1] + stack[-2]
    elif op == 'sub':
        regs[arg] = stack[-1] - stack[-2]
    elif op == 'mul':
        regs[arg] = stack[-1] * stack[-2]
    elif op == 'div':
        regs[arg] = stack[-1] // stack[-2]
    elif op == 'mod':
        regs[arg] = stack[-1] % stack[-2]
    elif op == 'xor':
        regs[arg] = stack[-1] ^ stack[-2]
    elif op == 'end':
        print('END DETECTED')
        print(regs[0])
        s.add(regs[0] == 0)

for op, arg in insts[:1976]:
    run(op, arg)

for op, arg in insts[1976:]:
    # if arg is not None:
    #     print(op, arg)
    # else:
    #     print(op)
    run(op, arg)
    # print(regs, stack[-10:])
    # print(op, arg)
    # print(regs, stack)

if s.check() == sat:
    print(''.join([chr(s.model()[f].as_long()) for f in flag]))
else:
    print('unsat')
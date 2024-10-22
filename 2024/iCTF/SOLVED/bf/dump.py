from z3 import *
import sys

s = Solver()
mem = [0] * 1000000
i = 1000

flag = [BitVec(f'flag_{i}', 8) for i in range(30)]
flag_i = 0  
def read_chr():
    global flag_i
    ret = flag[flag_i]
    flag_i += 1
    return ret

mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 118) & 0xFF


s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 87) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 4) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 96) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 84) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 17) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 82) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 8) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 8) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 143) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 13) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 96) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 4) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 108) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 6) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 174) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 85) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 9) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 142) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 128) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 17) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 154) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 86) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 8) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 152) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 6) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 118) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 8) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 148) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 9) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 83) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 6) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 123) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 9) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 158) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 111) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 131) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 7) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 86) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 10) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 6) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 144) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 17) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 103) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 11) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 4) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 161) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 23) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 2) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 113) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 23) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 138) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 19) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 3) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 101) & 0xFF
s.add(mem[i] == 0)
mem[i] = read_chr()
mem[i + 2] = (mem[i + 2] + 6) & 0xFF
mem[i + 1] = (mem[i + 1] + mem[i + 2] * 5) & 0xFF
mem[i + 2] = 0
mem[i] = (mem[i] + mem[i + 1] * 1) & 0xFF
mem[i + 1] = 0
mem[i] = (mem[i] + 101) & 0xFF
s.add(mem[i] == 0)

s.add(mem[i] == 0)

if s.check() == sat:
    m = s.model()
    print(''.join([chr(m[flag[i]].as_long()) for i in range(30)]))
else:
    print('unsat')

exit()
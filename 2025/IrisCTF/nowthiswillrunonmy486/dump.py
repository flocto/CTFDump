import z3
from libdebug import debugger

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(0x20)]
s = z3.Solver()
for i in range(0x20):
    s.add(flag[i] >= 0x20)
    s.add(flag[i] <= 0x7e)

x = 0
for i in range(0x20):
    x = x + z3.ZeroExt(24, flag[i])
s.add(x == 3327)

# 0xcc38c2be != (0xbf51b0d7 ^ *(&flag))
x = z3.Concat(*flag[:4][::-1])
s.add(0xcc38c2be == 0xbf51b0d7 ^ x)

# if (0xeaa2018 != (0x75cc547b ^ *(&data_2004 + arg5)) == 0)
x = z3.Concat(*flag[4:8][::-1])
s.add(0xeaa2018 == 0x75cc547b ^ x)

# if (0x1078b74d != (0x4f0fd83a ^ *(&jump_table_2008 + arg5)) == 0)
x = z3.Concat(*flag[8:12][::-1])
s.add(0x1078b74d == 0x4f0fd83a ^ x)

# (0xdb631232 != (0xa2117744 ^ *(&jump_table_2008[1] + arg5)) == 0)
x = z3.Concat(*flag[12:16][::-1])
s.add(0xdb631232 == 0xa2117744 ^ x)

# (0x98a0a199 != (0xecd0cec6 ^ *(&jump_table_2008[2] + arg5)) == 0)
x = z3.Concat(*flag[16:20][::-1])
s.add(0x98a0a199 == 0xecd0cec6 ^ x)

# (0x42789493 != (0x2e19f9fa ^ *(&jump_table_2008[3] + arg5)) == 0)
x = z3.Concat(*flag[20:24][::-1])
s.add(0x42789493 == 0x2e19f9fa ^ x)

# (0x5685e086 != (0x32ea83d9 ^ *(&jump_table_2008[4] + arg5)) == 0)
x = z3.Concat(*flag[24:28][::-1])
s.add(0x5685e086 == 0x32ea83d9 ^ x)

# (0x98ca4085 != (0xe5eb61e0 ^ *(&jump_table_2008[5] + arg5)) == 0)
x = z3.Concat(*flag[28:32][::-1])
s.add(0x98ca4085 == 0xe5eb61e0 ^ x)

if s.check() != z3.sat:
    print('No solution')
    exit()

m = s.model()
flag = bytes(m[flag[i]].as_long() for i in range(0x20))
print(flag)

data = open('chal', 'rb').read()
start = data.find(b'\x17\x00\x00\x00\x10\x00\x00\x00')
size = 0x378

d = debugger('./chal')
r = d.run()
r.sendline(flag)
d.breakpoint(0x17b0, file='binary')
d.cont()
addr = d.regs.rdi
d.breakpoint(0x1806, file='binary')
d.cont()
dump = d.mem[addr, size]
d.terminate()

data = data[:start] + dump + data[start+size:]
open('dump.bin', 'wb').write(data)
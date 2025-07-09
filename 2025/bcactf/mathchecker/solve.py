from z3 import *

s = Solver()
buf = [BitVec(f'buf_{i}', 8) for i in range(10)]

for i in range(10):
    s.add(buf[i] >= 0x30, buf[i] <= 0x39)

def zxd(x):
    return ZeroExt(24, x)

# syscall(sys_read {3}, fd: 0, buf: &buf, count: 0xa)
# int32_t b1*5 = (zx.d(buf[1][0]) - 0x30) * 5
# if (b1*5.b == 40)

tmp = (zxd(buf[1]) - 0x30) * 5
s.add(tmp == 40)

#     int32_t eax_6 = (zx.d(buf[2][0]) - 0x30) * 0x10 + 2
#     int32_t edx_1 = 0

eax_6 = (zxd(buf[2]) - 0x30) * 0x10 + 2

#     if (divs.dp.d(edx_1:eax_6, 0x1a) == 5 && mods.dp.d(edx_1:eax_6, 0x1a) == 0
#             && zx.d(buf[0]) == '1')

# s.add(eax_6 // 0x1a == 5)
# s.add(eax_6 % 0x1a == 0)
s.add(eax_6 == 0x1a * 5 + 0)
s.add(buf[0] == 0x31)  # '1'

#         int32_t eax_15 =
#             b1*5 + (zx.d(buf[3][0]) - 0x30) * 0xa + zx.d(buf[4][0]) - 0x30
#         int32_t edx_3 = 0

eax_15 = tmp + (zxd(buf[3]) - 0x30) * 0xa + (zxd(buf[4]) - 0x30)
        
#         if (divs.dp.d(edx_3:eax_15, 0x13) == 7
#                 && mods.dp.d(edx_3:eax_15, 0x13) == 0)

s.add(eax_15 == 0x13 * 7 + 0) 

#             int32_t eax_19 = (zx.d(buf[6][0]) - 0x30) * 5
#             if (eax_19.b == 0x28)

eax_19 = (zxd(buf[6]) - 0x30) * 5
s.add(eax_19 == 0x28)

#                 int32_t eax_24 = (zx.d(buf[7][0]) - 0x30) * 0x10 + 2
#                 int32_t edx_5 = 0

eax_24 = (zxd(buf[7]) - 0x30) * 0x10 + 2
                
#                 if (divs.dp.d(edx_5:eax_24, 0x1a) == 5
#                         && mods.dp.d(edx_5:eax_24, 0x1a) == 0
#                         && zx.d(buf[5][0]) == 0x32)

s.add(eax_24 == 0x1a * 5 + 0)
s.add(buf[5] == 0x32)  # '2'


#                     int32_t eax_33 = eax_19 + (zx.d(buf[8][0]) - 0x30) * 0xa
#                         + zx.d(buf[9][0]) - 0x30
#                     int32_t edx_7 = 0

eax_33 = eax_19 + (zxd(buf[8]) - 0x30) * 0xa + (zxd(buf[9]) - 0x30)
                    
#                     if (divs.dp.d(edx_7:eax_33, 0x13) == 7
#                             && mods.dp.d(edx_7:eax_33, 0x13) == 0)

s.add(eax_33 == 0x13 * 7 + 0)

#                         noreturn end() __tailcall

# ❓️      syscall(sys_write {4}, fd: 1, buf: &fail_msg, count: 1)
# print_newline()
# syscall(sys_exit {1}, status: 1)
# noreturn

if s.check() == sat:
    m = s.model()
    flag = ''.join(chr(m[buf[i]].as_long()) for i in range(10))
    print(f'Flag: {flag}')
else:
    print('No solution found')
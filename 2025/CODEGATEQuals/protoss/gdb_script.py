import gdb
import time

inp = '''3.37.15.100:50051
10'''

open('input.txt', 'w').write(inp)

gdb.execute('run < input.txt')
gdb.execute('ignore 5 2')
# set $rax = "mmQJfqw5HJqfAGV3ftrV.2c5358d4b98d31e9"
# gdb.execute('set $rax = "mmQJfqw5HJqfAGV3ftrV.2c5358d4b98d31e9"')
# gdb.execute('c')

gdb.execute('set $rax = "commander"')
gdb.execute('set $rbx = 9')
gdb.execute('set $rcx = 0xdead')

gdb.execute('c')

# 0x80f110
# set rax = 0093c280
# gdb.execute('set $rax = 0x0093c280')
# gdb.execute('c')

# # 0x80f185
time.sleep(0.025)

# # $r9 now contains the struct we want
# # set r9 + 0x18 to pointer to "My_1ife_F0r_Aiur!!"
# 00d5f000 is same memory to write to
gdb.execute('set *($r9 + 0x18) = 0x00d5f000')
gdb.execute("set {char}0x00d5f000 = 'M'")
gdb.execute("set {char}0x00d5f001 = 'y'")
gdb.execute("set {char}0x00d5f002 = '_'")
gdb.execute("set {char}0x00d5f003 = '1'")
gdb.execute("set {char}0x00d5f004 = 'i'")
gdb.execute("set {char}0x00d5f005 = 'f'")
gdb.execute("set {char}0x00d5f006 = 'e'")
gdb.execute("set {char}0x00d5f007 = '_'")
gdb.execute("set {char}0x00d5f008 = 'F'")
gdb.execute("set {char}0x00d5f009 = '0'")
gdb.execute("set {char}0x00d5f00a = 'r'")
gdb.execute("set {char}0x00d5f00b = '_'")
gdb.execute("set {char}0x00d5f00c = 'A'")
gdb.execute("set {char}0x00d5f00d = 'i'")   
gdb.execute("set {char}0x00d5f00e = 'u'")
gdb.execute("set {char}0x00d5f00f = 'r'")
gdb.execute("set {char}0x00d5f010 = '!'")
gdb.execute("set {char}0x00d5f011 = '!'")
gdb.execute("set {char}0x00d5f012 = 0")
gdb.execute('set *($r9 + 0x20) = 18')

# gdb.execute('set *($r9 + 0x18) = 1')

# # set r8 to 0092f1e0
# gdb.execute('set $r8 = 0x092f1e0')

# # set r10 0092f2a0
# gdb.execute('set $r10 = 0x092f2a0')

# change grpc endpoint
gdb.execute('set $rdi = "/secret.SecretService/Flag"')
gdb.execute('set $rsi = 26')

gdb.execute('c')



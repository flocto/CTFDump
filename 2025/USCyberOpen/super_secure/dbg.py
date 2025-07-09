from libdebug import debugger
from libdebug.state.thread_context import ThreadContext
from libdebug.data.breakpoint import Breakpoint
from pwn import *

d = debugger(argv=['./super_secure', 'hello'])
pipe = d.run()

s = b''
def fill_s(t: ThreadContext, bp: Breakpoint):
    global s
    # print("Filling s")
    # write to rbp-0x50
    start = t.regs.rbp - 0x50
    t.mem.write(start, s)

d.breakpoint(0x14d7, callback=fill_s, file="binary")

val = 0
dump = None
def read_val(t: ThreadContext, bp: Breakpoint):
    # print("Reading val")
    global val
    # read from rax
    val = t.regs.rax

    # read mem @ 0x6dd
    rip = t.regs.rip
    base = rip - 0x559
    # print(f"RIP: {hex(rip)}")
    global dump
    dump = t.mem.read(base + 0x6dd, 0x20000)

d.breakpoint(0x1559, callback=read_val, file="binary")

r = process(['./super_secure', 'hello'])
challenge = r.recvline_contains('challenge: ').decode().strip().split(': ', 1)[1].encode()

d.cont()
import time
time.sleep(1.5) 
pipe.sendlineafter(b'>', b'1')
d.wait()

print(dump[:0x100].hex())

print(hex(val))
r.sendlineafter(b'>', str(val).encode())
r.interactive()


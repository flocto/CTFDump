from unicorn import *
from unicorn.x86_const import *
import capstone
import struct as st

data = open('serpentine.exe', 'rb').read()

start = 0x95ef0
length = 0x800000
data = data[start:start+length]

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def print_red(s):
    print(f'\033[91m{s}\033[0m')

def print_yellow(s):
    print(f'\033[93m{s}\033[0m')

def make_struct(offset):
    nxt = offset + 1
    c = nxt + data[nxt] + 1
    if c & 1:
        c += 1
    return (offset, nxt, c)

def find_ret_addr(struct):
    v30 = struct[2]
    #  v31 = (unsigned __int8)v30[2];
    #     v32 = v31 + 1;
    #     if ( (v31 & 1) == 0 )
    #       v32 = (unsigned __int8)v30[2];
    #     *a7 = &v30[2 * (v32 + 2) + 4];
    #     v76 = a2 + *(unsigned int *)&v30[2 * v32 + 4];
    v31 = data[v30 + 2]
    v32 = v31 + 1
    if v31 & 1 == 0:
        v32 = data[v30 + 2]

    v76 = st.unpack("<I", data[v30 + 2 * v32 + 4:v30 + 2 * (v32 + 2) + 4])[0]
    return v76

def dump_regs(uc):
    print(f"RAX: 0x{uc.reg_read(UC_X86_REG_RAX):016x}          | R8:  0x{uc.reg_read(UC_X86_REG_R8):016x}")
    print(f"RBX: 0x{uc.reg_read(UC_X86_REG_RBX):016x}          | R9:  0x{uc.reg_read(UC_X86_REG_R9):016x}")
    print(f"RCX: 0x{uc.reg_read(UC_X86_REG_RCX):016x}          | R10: 0x{uc.reg_read(UC_X86_REG_R10):016x}")
    print(f"RDX: 0x{uc.reg_read(UC_X86_REG_RDX):016x}          | R11: 0x{uc.reg_read(UC_X86_REG_R11):016x}")
    print(f"RBP: 0x{uc.reg_read(UC_X86_REG_RBP):016x}          | R12: 0x{uc.reg_read(UC_X86_REG_R12):016x}")
    print(f"RSP: 0x{uc.reg_read(UC_X86_REG_RSP):016x}          | R13: 0x{uc.reg_read(UC_X86_REG_R13):016x}")
    print(f"RSI: 0x{uc.reg_read(UC_X86_REG_RSI):016x}          | R14: 0x{uc.reg_read(UC_X86_REG_R14):016x}")
    print(f"RDI: 0x{uc.reg_read(UC_X86_REG_RDI):016x}          | R15: 0x{uc.reg_read(UC_X86_REG_R15):016x}")

def dump_stack(uc, size=0x40):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    for i in range(0, size + 1, 8):
        print(f"0x{rsp + i:x}: 0x{st.unpack('<Q', uc.mem_read(rsp + i, 8))[0]:016x}")

def pack_context(uc: Uc):
    context = b'\x00' * (48 + 4) # P1Home - P6Home + ContextFlags
    context += st.pack('<H', uc.reg_read(UC_X86_REG_MXCSR)) # MxCsr
    context += st.pack('<H', uc.reg_read(UC_X86_REG_CS)) # SegCs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_DS)) # SegDs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_ES)) # SegEs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_FS)) # SegFs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_GS)) # SegGs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_SS)) # SegSs
    context += st.pack('<I', uc.reg_read(UC_X86_REG_EFLAGS)) # EFlags
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR0)) # Dr0 
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR1)) # Dr1
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR2)) # Dr2
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR3)) # Dr3
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR6)) # Dr6
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR7)) # Dr7
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RAX)) # Rax
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RCX)) # Rcx
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RDX)) # Rdx
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RBX)) # Rbx
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RSP)) # Rsp
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RBP)) # Rbp
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RSI)) # Rsi
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RDI)) # Rdi
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R8)) # R8
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R9)) # R9
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R10)) # R10
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R11)) # R11
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R12)) # R12
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R13)) # R13
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R14)) # R14
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R15)) # R15
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RIP)) # Rip
    return context

def extract_inst(uc: Uc, func, call_addr, expected_return, print=lambda x:None):
    insts = list(cs.disasm(func, call_addr))
    # for i in insts:
    #     print(f"0x{i.address:x}: {i.mnemonic} {i.op_str}")
    #     input('> ')

    # pop qword ptr [rip + ?] <- this pop gets the rax stored from call, so basically the expected return
    pop_qword = insts[0]
    inner = pop_qword.op_str.split('[')[1].split(']')[0]
    sign = 1 if '+' in inner else -1
    offset = int(inner.split(' ')[-1], 16) * sign
    write_addr = pop_qword.address + pop_qword.size + offset
    print(f'write_addr: 0x{write_addr:x}')
    uc.mem_write(write_addr, st.pack('<Q', expected_return))

    # push rax -> do nothing
    assert f'{insts[1].mnemonic} {insts[1].op_str}' == 'push rax'

    # mov rax, 0 -> do nothing
    assert f'{insts[2].mnemonic} {insts[2].op_str}' == 'mov rax, 0'

    # mov ah, byte ptr [rip - ?] -> load byte from rip - ? to ah, USUALLY this is the low byte stored by the first pop qword of the PREVIOUS subcall
    mov_ah = insts[3]
    inner = mov_ah.op_str.split('[')[1].split(']')[0]
    sign = 1 if '+' in inner else -1
    offset = int(inner.split(' ')[-1], 16) * sign
    read_addr = mov_ah.address + mov_ah.size + offset
    print(f'read_addr: 0x{read_addr:x}')
    ah = uc.mem_read(read_addr, 1)[0]
    eax = ah << 8

    # lea eax, [eax +/- ?] -> change eax
    lea_eax = insts[4]
    inner = lea_eax.op_str.split('[')[1].split(']')[0]
    sign = 1 if '+' in inner else -1
    offset = int(inner.split(' ')[-1], 16) * sign
    eax += offset
    eax &= 0xffffffff
    print(f'eax: 0x{eax:x}')

    # mov dword ptr [rip + 1], eax -> store eax
    assert f'{insts[5].mnemonic} {insts[5].op_str}' == 'mov dword ptr [rip + 1], eax'
    uc.mem_write(insts[5].address + insts[5].size + 1, st.pack('<I', eax))
    
    # pop rax -> do nothing
    assert f'{insts[6].mnemonic} {insts[6].op_str}' == 'pop rax'

    # get real instruction + rest
    later_insts = uc.mem_read(insts[6].address + insts[6].size, 0x1000)
    later_insts = list(cs.disasm(later_insts, insts[6].address + insts[6].size))

    real_inst = later_insts[0]
    if real_inst.mnemonic == 'jmp':
        # jmps early, return now
        jmp_addr = int(real_inst.op_str.split(' ')[-1], 16)
        return real_inst, jmp_addr

    # mov dword ptr [rip - ?], dat -> overwrite real inst with fake inst
    inner = later_insts[1].op_str.split('[')[1].split(']')[0]
    sign = 1 if '+' in inner else -1
    offset = int(inner.split(' ')[-1], 16) * sign
    dat = int(later_insts[1].op_str.split(' ')[-1], 16)
    write_addr = later_insts[1].address + later_insts[1].size + offset
    print(f'write_addr: 0x{write_addr:x}, dat: 0x{dat:x}')
    uc.mem_write(write_addr, st.pack('<I', dat))

    # push rax -> do nothing, still the old rax
    assert f'{later_insts[2].mnemonic} {later_insts[2].op_str}' == 'push rax'

    # mov rax, ? -> start of real return
    ret_addr = int(later_insts[3].op_str.split(' ')[-1], 16)

    # lea rax, [rax +/- ?] -> change rax
    if later_insts[4].op_str != 'rax, [rax]':
        inner = later_insts[4].op_str.split('[')[1].split(']')[0]
        sign = 1 if '+' in inner else -1
        offset = int(inner.split(' ')[-1], 16) * sign
        ret_addr += offset

    # xchg qword ptr [rsp], rax -> puts new return on stack, loads old rax
    assert f'{later_insts[5].mnemonic} {later_insts[5].op_str}' == 'xchg qword ptr [rsp], rax'

    # ret
    assert later_insts[6].mnemonic == 'ret'

    return real_inst, ret_addr

extracted = b''
branch = {}
def step(uc: Uc, addr, size, user_data):
    global extracted, branch
    insts = uc.mem_read(addr, 0x1000)
    # print(f"0x{addr:x}[{size}]: {inst.hex()}")

    for inst in cs.disasm(insts, addr):
        if inst.mnemonic == 'call':
            # print('Call found, extracting real instruction and return')

            call_addr = int(inst.op_str, 16)
            # print(f'Call addr: 0x{call_addr:x}')
            
            subcall = uc.mem_read(call_addr, 0x1000)
            expected_return = inst.address + inst.size
            real_inst, ret_addr = extract_inst(uc, subcall, call_addr, expected_return)

            # print('===REAL INST===')    
            # print_red(f'0x{real_inst.address:x}: {real_inst.mnemonic} {real_inst.op_str}')
            # print(f'jmp: 0x{ret_addr:x}')
            
            if real_inst.mnemonic == 'sub':
                print_red(f'0x{real_inst.address:x}: {real_inst.mnemonic} {real_inst.op_str}')

            elif real_inst.mnemonic != 'jmp':
                # only add if not jmp
                print(f'0x{real_inst.address:x}: {real_inst.mnemonic} {real_inst.op_str}')
                if 'rip' in real_inst.op_str:
                    print(f'0x{real_inst.address:x}: {real_inst.mnemonic} {real_inst.op_str}')
                    inner = real_inst.op_str.split('[')[1].split(']')[0]
                    sign = 1 if '+' in inner else -1
                    offset = int(inner.split(' ')[-1], 16) * sign
                    b_addr = real_inst.address + real_inst.size + offset
                    reg = real_inst.op_str.split(',')[0]
                    branch[reg] = b_addr
                    extracted += real_inst.bytes[:3] + b'\x07\x00\x00\x00'
                else:
                    extracted += real_inst.bytes
            else:
                print_yellow(f'0x{real_inst.address:x}: {real_inst.mnemonic} {real_inst.op_str}')

            uc.reg_write(UC_X86_REG_RIP, ret_addr)
            break

        elif inst.mnemonic == 'hlt':
            jmp = find_ret_addr(make_struct(inst.address))
            # print(f"jmp: 0x{jmp:x}")
            # add nothing to extracted, jmps are not real instructions
            context = pack_context(uc)
            uc.reg_write(UC_X86_REG_RIP, jmp)
            break

        elif inst.mnemonic == 'jmp':
            print(inst.op_str, branch)
            if input('> ') == 'q':
                uc.emu_stop()
                return
            if inst.op_str in branch:
                jmp_addr = branch[inst.op_str]
                uc.reg_write(UC_X86_REG_RIP, jmp_addr)
                extracted += inst.bytes
            else:
                try:
                    jmp_addr = int(inst.op_str.split(' ')[-1], 16)
                    uc.reg_write(UC_X86_REG_RIP, jmp_addr)
                    # print(f'jmp: 0x{jmp_addr:x}')
                except Exception as e:
                    print(e)
                    uc.emu_stop()
                    return
                break
        
        else:
            # if 'rip' in inst.op_str:
            print(f"0x{inst.address:x}: {inst.mnemonic} {inst.op_str}")
            extracted += inst.bytes

        # if input('> ') == 'q':
        #     uc.emu_stop()
        #     break

    # print('===REGS===')
    # dump_regs(uc)
    # print('===STACK===')
    # dump_stack(uc)
    # print('===========')


inp = b"AAAA0000BBBB1111CCCC2222DDDD3333"
_key_input = 0x000000014089b8e8

mu = Uc(UC_ARCH_X86, UC_MODE_64)

mu.mem_map(0, length, UC_PROT_ALL)
mu.mem_write(0, data)

# init
mu.mem_map(_key_input & 0xfffffffffffff000, 0x1000)
mu.mem_write(_key_input, inp)

# stack
mu.mem_map(0x6710000, 0x100000)
mu.reg_write(UC_X86_REG_RSP, 0x67FFEA8)

mu.reg_write(UC_X86_REG_RAX, _key_input)
mu.reg_write(UC_X86_REG_RCX, _key_input)

# step one instruction at a time
hook = mu.hook_add(UC_HOOK_CODE, step)

mu.emu_start(0, length)

extracted += b'\xc3' # ret
old = open('serpentine.exe', 'rb').read()
patched = old[:start] + extracted + old[start+len(extracted):]
open('patched.exe', 'wb').write(patched)
from unicorn import *
from unicorn.x86_const import *
import capstone
import struct as st
import ctypes

def print_red(s):
    print(f'\033[91m{s}\033[0m')

def print_yellow(s):
    print(f'\033[93m{s}\033[0m')

data = open('serpentine.exe', 'rb').read()

data_section = 0x20400
data_section_length = 0x876800
_data = data[data_section:data_section+data_section_length]

start = 0x95ef0
length = 0x800000
data = data[start:start+length]


cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

class RUNTIME_FUNCTION(ctypes.Structure):
    _fields_ = [
        ('begin', ctypes.c_ulong),
        ('end', ctypes.c_ulong),
        ('info', ctypes.c_ulong),
    ]

def make_struct(offset):
    nxt = offset + 1
    c = nxt + data[nxt] + 1
    if c & 1:
        c += 1
    # return (offset, nxt, c)
    return RUNTIME_FUNCTION(offset, nxt, c)

class UnwindInfo(ctypes.Structure):
    _fields_ = [
        ('version', ctypes.c_ubyte, 3),
        ('flags', ctypes.c_ubyte, 5),
        ('prolog_size', ctypes.c_ubyte),
        ('count', ctypes.c_ubyte),
        ('frame_reg', ctypes.c_ubyte),
    ]

class UnwindCode(ctypes.Structure):
    _fields_ = [
        ('CodeOffset', ctypes.c_ubyte),
        ('UnwindOp', ctypes.c_ubyte, 4),
        ('OpInfo', ctypes.c_ubyte, 4),
    ]


unwind_code_names = [
    'UWOP_PUSH_NONVOL',
    'UWOP_ALLOC_LARGE',
    'UWOP_ALLOC_SMALL',
    'UWOP_SET_FPREG',
    'UWOP_SAVE_NONVOL',
    'UWOP_SAVE_NONVOL_FAR',
    '', # 6
    '', # 7
    'UWOP_SAVE_XMM128',
    'UWOP_SAVE_XMM128_FAR',
    'UWOP_PUSH_MACHFRAME',
]
unwind_reg_map = [
    'RAX',
    'RCX',  
    'RDX',
    'RBX',
    'RSP',
    'RBP',
    'RSI',
    'RDI',
    'R8',
    'R9',
    'R10',
    'R11',
    'R12',
    'R13',
    'R14',
    'R15',
]
def disas_unwind_codes(data):
    unwind_codes = []
    i = 0
    while i < len(data):
        unwind_code = UnwindCode.from_buffer_copy(data[i:i+2])

        # print(f"CodeOffset: {unwind_code.CodeOffset:x}")
        # print(f"UnwindOp: {unwind_code.UnwindOp:x}")
        # print(f"OpInfo: {unwind_code.OpInfo:x}")

        unwind_code.name = unwind_code_names[unwind_code.UnwindOp]

        match unwind_code.UnwindOp:
            case 0:
                unwind_codes.append((unwind_code.UnwindOp, unwind_code.OpInfo, unwind_reg_map[unwind_code.OpInfo]))
            case 1:
                if unwind_code.OpInfo == 0:
                    unwind_codes.append((unwind_code.UnwindOp, st.unpack('<H', data[i+2:i+4])[0])) 
                    i += 2
                else:
                    unwind_codes.append((unwind_code.UnwindOp, st.unpack('<I', data[i+2:i+6])[0])) 
                    i += 4
            case 2:
                unwind_codes.append((unwind_code.UnwindOp, unwind_code.OpInfo * 8 + 8)) 
            case 3:
                unwind_codes.append((unwind_code.UnwindOp, unwind_code.OpInfo * 16)) 
            case 4:
                unwind_codes.append((unwind_code.UnwindOp, unwind_reg_map[unwind_code.OpInfo], st.unpack('<H', data[i+2:i+4])[0])) 
                i += 2
            case 5:
                unwind_codes.append((unwind_code.UnwindOp, unwind_reg_map[unwind_code.OpInfo], st.unpack('<I', data[i+2:i+6])[0])) 
                i += 4
            case 8:
                unwind_codes.append((unwind_code.UnwindOp, unwind_reg_map[unwind_code.OpInfo], st.unpack('<H', data[i+2:i+4])[0])) 
                i += 2
            case 9:
                unwind_codes.append((unwind_code.UnwindOp, unwind_reg_map[unwind_code.OpInfo], st.unpack('<I', data[i+2:i+6])[0])) 
                i += 4
            case 10:
                unwind_codes.append((unwind_code.UnwindOp, unwind_code.OpInfo))

        i += 2
        # print(f'{unwind_code.name} {unwind_codes[-1][1]}')
    return unwind_codes

uc_reg_map = [
    UC_X86_REG_RAX,
    UC_X86_REG_RCX,
    UC_X86_REG_RDX,
    UC_X86_REG_RBX,
    UC_X86_REG_RSP,
    UC_X86_REG_RBP,
    UC_X86_REG_RSI,
    UC_X86_REG_RDI,
    UC_X86_REG_R8,
    UC_X86_REG_R9,
    UC_X86_REG_R10,
    UC_X86_REG_R11,
    UC_X86_REG_R12,
    UC_X86_REG_R13,
    UC_X86_REG_R14,
    UC_X86_REG_R15,
]
def parse_unwind_codes(uc: Uc, unwind_codes, frame_reg):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    for opcode, *args in unwind_codes:
        print(f'{unwind_code_names[opcode]} {args}')
        match opcode:
            case 0: # UWOP_PUSH_NONVOL
                uc.reg_write(uc_reg_map[args[0]], st.unpack('<Q', uc.mem_read(rsp, 8))[0])
                rsp += 8
            case 1: # UWOP_ALLOC_LARGE
                rsp += args[0]
            case 3: # UWOP_SET_FPREG
                # print('UWOP_SET_FPREG')
                pass
            case 10: # UWOP_PUSH_MACHFRAME
                if args[0] == 0:
                    rsp = st.unpack('<Q', uc.mem_read(rsp + 0x18, 8))[0]
                else:
                    rsp = st.unpack('<Q', uc.mem_read(rsp + 0x20, 8))[0] 
                # print(f'old_rsp: 0x{old_rsp:x}')
                # print(f'data @ old_rsp: 0x{st.unpack("<Q", uc.mem_read(old_rsp, 8))[0]:x}')
            case _:
                raise ValueError(f'Unknown opcode: {opcode}')


def parse_unwind_info(runtime_func):
    unwind_info_addr = runtime_func.info
    unwind_info = UnwindInfo.from_buffer_copy(data[unwind_info_addr:unwind_info_addr+4])
    version = unwind_info.version
    flags = unwind_info.flags
    print(f"version: {version:x}")
    print(f"flags: {flags:05b}")
    print(f"prolog_size: {unwind_info.prolog_size:x}")
    print(f"count: {unwind_info.count:x}")
    print(f"frame_reg: {unwind_info.frame_reg:x}")
    count = unwind_info.count
    count_adj = count + 1
    if count & 1 == 0:
        count_adj = count

    unwind_codes = []
    if count:
        unwind_codes = disas_unwind_codes(data[unwind_info_addr + 4:unwind_info_addr + 4 + count * 2])

    func_start = st.unpack("<I", data[unwind_info_addr + 2 * count_adj + 4:unwind_info_addr + 2 * (count_adj + 2) + 4])[0]
    return func_start, unwind_codes

def dump_regs(uc: Uc):
    print(f"RAX: 0x{uc.reg_read(UC_X86_REG_RAX):016x}          | R8:  0x{uc.reg_read(UC_X86_REG_R8):016x}")
    print(f"RBX: 0x{uc.reg_read(UC_X86_REG_RBX):016x}          | R9:  0x{uc.reg_read(UC_X86_REG_R9):016x}")
    print(f"RCX: 0x{uc.reg_read(UC_X86_REG_RCX):016x}          | R10: 0x{uc.reg_read(UC_X86_REG_R10):016x}")
    print(f"RDX: 0x{uc.reg_read(UC_X86_REG_RDX):016x}          | R11: 0x{uc.reg_read(UC_X86_REG_R11):016x}")
    print(f"RBP: 0x{uc.reg_read(UC_X86_REG_RBP):016x}          | R12: 0x{uc.reg_read(UC_X86_REG_R12):016x}")
    print(f"RSP: 0x{uc.reg_read(UC_X86_REG_RSP):016x}          | R13: 0x{uc.reg_read(UC_X86_REG_R13):016x}")
    print(f"RSI: 0x{uc.reg_read(UC_X86_REG_RSI):016x}          | R14: 0x{uc.reg_read(UC_X86_REG_R14):016x}")
    print(f"RDI: 0x{uc.reg_read(UC_X86_REG_RDI):016x}          | R15: 0x{uc.reg_read(UC_X86_REG_R15):016x}")

def dump_stack(uc: Uc, size=0x40):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    for i in range(0, size + 1, 8):
        d = st.unpack('<Q', uc.mem_read(rsp + i, 8))[0]
        print(f"0x{rsp + i:x}: 0x{d:016x}", end=' ')
        if d >= 0x140022000 and d <= 0x1408b0000:
            at_d = uc.mem_read(d, 8)
            print(f'-> 0x{st.unpack("<Q", at_d)[0]:016x}')
        else:
            print()

def pack_context(uc: Uc):
    context = b'\x00' * (48 + 4) # P1Home - P6Home + ContextFlags
    # 0x34
    context += st.pack('<I', uc.reg_read(UC_X86_REG_MXCSR)) # MxCsr
    context += st.pack('<H', uc.reg_read(UC_X86_REG_CS)) # SegCs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_DS)) # SegDs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_ES)) # SegEs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_FS)) # SegFs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_GS)) # SegGs
    context += st.pack('<H', uc.reg_read(UC_X86_REG_SS)) # SegSs
    # 0x40
    context += st.pack('<I', uc.reg_read(UC_X86_REG_EFLAGS)) # EFlags
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR0)) # Dr0 
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR1)) # Dr1
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR2)) # Dr2
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR3)) # Dr3
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR6)) # Dr6
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_DR7)) # Dr7
    # 0x78
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RAX)) # Rax
    # 0x80
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RCX)) # Rcx
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RDX)) # Rdx
    # 0x90
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RBX)) # Rbx
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RSP)) # Rsp
    # 0xa0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RBP)) # Rbp
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RSI)) # Rsi
    # 0xb0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RDI)) # Rdi
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R8)) # R8
    # 0xc0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R9)) # R9
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R10)) # R10
    # 0xd0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R11)) # R11
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R12)) # R12
    # 0xe0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R13)) # R13
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R14)) # R14
    # 0xf0
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_R15)) # R15
    context += st.pack('<Q', uc.reg_read(UC_X86_REG_RIP)) # Rip
    return context

def do_hlt_things(uc: Uc, context, jmp, rsp):
    # shift stack down 0xeb0
    uc.reg_write(UC_X86_REG_RSP, rsp - 0xeb0)
    # write context to + 0xa8
    uc.mem_write(rsp - 0xeb0 + 0xa8, context)
    # write ptr to context at + 0x610
    uc.mem_write(rsp - 0xeb0 + 0x610, st.pack('<Q', rsp - 0xeb0 + 0xa8))
    # set r9 to ptr - 0x28
    uc.reg_write(UC_X86_REG_R9, rsp - 0xeb0 + 0x5e8)
    # set rax, rip to jmp
    uc.reg_write(UC_X86_REG_RIP, jmp)
    uc.reg_write(UC_X86_REG_RAX, jmp)
    # clear these registers
    uc.reg_write(UC_X86_REG_RBX, 0)
    uc.reg_write(UC_X86_REG_RDI, 0)
    uc.reg_write(UC_X86_REG_R10, 0)
    uc.reg_write(UC_X86_REG_R11, 0x100000)
    uc.reg_write(UC_X86_REG_R12, 0)
    uc.reg_write(UC_X86_REG_R14, 0)
    # set rcx = r9 + 0x690
    uc.reg_write(UC_X86_REG_RCX, uc.reg_read(UC_X86_REG_R9) + 0x690)
    # set rdx = old rsp
    uc.reg_write(UC_X86_REG_RDX, rsp)
    # set rbp = r9 - 0x50
    uc.reg_write(UC_X86_REG_RBP, uc.reg_read(UC_X86_REG_R9) - 0x50)
    # set rsi = r9 + 0x690
    uc.reg_write(UC_X86_REG_RSI, uc.reg_read(UC_X86_REG_RCX))
    # set r8 = r9 + 0x1a0
    uc.reg_write(UC_X86_REG_R8, uc.reg_read(UC_X86_REG_R9) + 0x1a0)
    # set r13 = context ptr
    uc.reg_write(UC_X86_REG_R13, rsp - 0xec0 + 0xa8)
    # set r15 = r9 + 0x1a0
    uc.reg_write(UC_X86_REG_R15, uc.reg_read(UC_X86_REG_R8))




n = 8
last_n = []
def check_real_inst(last_n):
    # pop qword ptr [rip + ?]
    # push rax
    # mov rax, 0
    # mov ah, byte ptr [rip - ?]
    # lea eax, [eax +/- ?]
    # mov dword ptr [rip + ?], eax
    # pop rax
    if 'pop qword ptr [rip +' in last_n[0][1]:
        if 'push rax' in last_n[1][1]:
            if 'mov rax, 0' in last_n[2][1]:
                if 'mov ah, byte ptr [rip -' in last_n[3][1]:
                    if 'lea eax, [eax ' in last_n[4][1]:
                        if 'mov dword ptr [rip +' in last_n[5][1]:
                            if 'pop rax' in last_n[6][1]:
                                return True
    return False

in_call = False
in_call_insts = []
DEBUG = True
def step(uc: Uc, addr, size, user_data):
    global last_n, in_call, in_call_insts, DEBUG
    # real_inst = False
    inst = uc.mem_read(addr, size)
    inst = next(cs.disasm(inst, addr))

    # print_yellow(f'0x{addr:x}: {inst.mnemonic} {inst.op_str}')

    if last_n and f'0x{inst.address:x}: {inst.mnemonic} {inst.op_str}' == last_n[-1]:
        return # duplicate

    if in_call:
        if in_call_insts and in_call_insts[-1].address == inst.address: return # duplicate
        in_call_insts.append(inst)
        if inst.mnemonic == 'ret':
            # for f in in_call_insts:
            #     print(f'0x{f.address:x}: {f.mnemonic} {f.op_str}')
            in_call = False
            in_call_insts = []

        if len(in_call_insts) != 8:
            return
        elif inst.mnemonic == 'jmp':
            in_call = False
            in_call_insts = []
            # jmp to address
            jmp_addr = int(inst.op_str, 16)
            print(f'jmp: 0x{jmp_addr:x}')
            uc.reg_write(UC_X86_REG_RIP, jmp_addr)
            return


    if inst.mnemonic == 'call':
        in_call = True
        return 

    print('===REGS===')
    dump_regs(uc)
    print('===STACK===')
    dump_stack(uc)
    print('===========')

    for f in last_n:
        print(f)

    # if len(last_n) == n and check_real_inst(last_n):
    #     real_inst = True

    if size == 1 and inst.mnemonic == 'hlt':
        old_rsp = uc.reg_read(UC_X86_REG_RSP)
        in_call = 0
        jmp, unwind_codes = parse_unwind_info(make_struct(addr))
        if unwind_codes:
            print('===UNWIND===')
            parse_unwind_codes(uc, unwind_codes)
            input()

        print(f"jmp: 0x{jmp:x}")
        context = pack_context(uc)
        do_hlt_things(uc, context, jmp, old_rsp)

        # if input('> ') == 'q':
        #     uc.emu_stop() 
        #     return


    else:
        inst_str = f'0x{inst.address:x}: {inst.mnemonic} {inst.op_str}'
        print(inst_str)
        last_n.append(inst_str)

        while len(last_n) > n:
            last_n.pop(0)

    if DEBUG and input('> ') == 'q':
        uc.emu_stop()

inp = b"AAAA0000BBBB1111CCCC2222DDDD3333"
_key_input = 0x000000014089b8e8

mu = Uc(UC_ARCH_X86, UC_MODE_64)

mu.mem_map(0, length, UC_PROT_ALL)
mu.mem_write(0, data)

# data  {0x140022000-0x1408a6f18
mu.mem_map(0x140022000, 0x1408b0000 - 0x140022000)
mu.mem_write(0x140022000, _data)
mu.mem_write(_key_input, inp)

# stack
mu.mem_map(0x6710000, 0x100000)
mu.reg_write(UC_X86_REG_RSP, 0x67FFEA8)

mu.reg_write(UC_X86_REG_RAX, _key_input)
mu.reg_write(UC_X86_REG_RCX, _key_input)

# step one instruction at a time
hook = mu.hook_add(UC_HOOK_CODE, step)

mu.emu_start(0, length)
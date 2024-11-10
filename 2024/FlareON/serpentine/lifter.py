from unicorn import *
from unicorn.x86_const import *
import capstone
import struct as st
import ctypes
from pwn import asm, context, u64, u32
import re
from tqdm import tqdm
context.arch = 'amd64'

def print_red(s):
    print(f'\033[91m{s}\033[0m')

def print_yellow(s):
    print(f'\033[93m{s}\033[0m')

def print_grey(s):
    print(f'\033[90m{s}\033[0m')

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

data = open('serpentine.exe', 'rb').read()

data_section = 0x20400
data_section_length = 0x876800
_data = data[data_section:data_section+data_section_length]

start = 0x95ef0
length = 0x800000
data = data[start:start+length]

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
CONTEXT = {}
CONTEXT_PTRS = []
CONTEXT_BASE = 0x1408a0000
MXCSR = 0x1408a0034 

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

def parse_unwind_info(runtime_func):
    unwind_info_addr = runtime_func.info
    unwind_info = UnwindInfo.from_buffer_copy(data[unwind_info_addr:unwind_info_addr+4])
    # version = unwind_info.version
    # flags = unwind_info.flags
    # print(f"version: {version:x}")
    # print(f"flags: {flags:05b}")
    # print(f"prolog_size: {unwind_info.prolog_size:x}")
    # print(f"count: {unwind_info.count:x}")
    # print(f"frame_reg: {unwind_info.frame_reg:x}")
    count = unwind_info.count
    count_adj = count + 1
    if count & 1 == 0:
        count_adj = count

    unwind_codes = []
    if count:
        unwind_codes = disas_unwind_codes(data[unwind_info_addr + 4:unwind_info_addr + 4 + count * 2])

    func_start = st.unpack("<I", data[unwind_info_addr + 2 * count_adj + 4:unwind_info_addr + 2 * (count_adj + 2) + 4])[0]
    return func_start, unwind_codes, unwind_info.frame_reg

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
unwind_reg_map = [r.lower() for r in unwind_reg_map]
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
                    unwind_codes.append((unwind_code.UnwindOp, st.unpack('<H', data[i+2:i+4])[0] * 8)) 
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
def lift_unwind_codes(uc: Uc, unwind_codes, frame_reg):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    lifted_codes = [
        'push rax',
        'mov rax, rsp',
        'mov qword ptr [0x1408a2000], rax', 
        'pop rax'
    ]
    for opcode, *args in unwind_codes:
        # print(f'rsp: 0x{rsp:x}, {unwind_code_names[opcode]} {args}')
        # dump_stack(uc)
        # print(f'{unwind_code_names[opcode]} {args}')
        match opcode:
            case 0: # UWOP_PUSH_NONVOL
                reg = unwind_reg_map[args[0]]
                lifted_codes.append(f'pop {reg}')
                # pop reg
                # uc.reg_write(uc_reg_map[args[0]], u64(uc.mem_read(rsp, 8)))
            case 1: # UWOP_ALLOC_LARGE
                lifted_codes.append(f'; UWOP_ALLOC_LARGE {args[0]}')
                lifted_codes.append(f'add rsp, {args[0]}')
                # add rsp, args[0]
                # rsp += args[0]
            case 2: # `UWOP_ALLOC_SMALL`
                # lifted_codes.append(f'add rsp, {args[0] * 8 + 8}')
                lifted_codes.append(f'; UWOP_ALLOC_SMALL {args[0]}')
                lifted_codes.append(f'add rsp, {args[0]}')
            case 3: # UWOP_SET_FPREG
                lifted_codes.append(f'; UWOP_SET_FPREG {args[0]}, {unwind_reg_map[frame_reg]}')
                lifted_codes.append(f'mov rsp, {unwind_reg_map[frame_reg]}')
                lifted_codes.append(f'add rsp, {args[0] * 16}')
                # mov rsp, frame_reg
                # rsp = uc.reg_read(uc_reg_map[frame_reg])
                # rsp += args[0] * 16
            case 10: # UWOP_PUSH_MACHFRAME
                if args[0] == 0:
                    lifted_codes.append('mov rsp, qword ptr [rsp + 0x18]')
                    # mov rsp, qword ptr [rsp + 0x18]
                    # rsp = u64(uc.mem_read(rsp + 0x18, 8))
                else:
                    lifted_codes.append('mov rsp, qword ptr [rsp + 0x20]')
                    # mov rsp, qword ptr [rsp + 0x20]
                    # rsp = u64(uc.mem_read(rsp + 0x20, 8))
                # print(f'nxt rsp: 0x{rsp:x}')
            case _:
                raise ValueError(f'Unknown opcode: {opcode}')
    
    lifted_codes.append('push rax')
    lifted_codes.append('mov rax, qword ptr [0x1408a2000]')
    lifted_codes.append('xchg qword ptr [rsp], rax')
    lifted_codes.append('pop rsp')
    return lifted_codes

context_reg_offsets = {
    0x34: 'mxcsr',
    0x78: 'rax',
    0x80: "RCX".lower(),
    0x88: "RDX".lower(),
    0x90: "RBX".lower(),
    0x98: "RSP".lower(),
    0xa0: "RBP".lower(),
    0xa8: "RSI".lower(),
    0xb0: "RDI".lower(),
    0xb8: "R8".lower(),
    0xc0: "R9".lower(),
    0xc8: "R10".lower(),
    0xd0: "R11".lower(),
    0xd8: "R12".lower(),
    0xe0: "R13".lower(),
    0xe8: "R14".lower(),
    0xf0: "R15".lower(),
    0xf8: "RIP".lower(),
}
def pack_context(uc: Uc):
    global CONTEXT, CONTEXT_PTRS
    CONTEXT_PTRS = []
    CONTEXT[0x34] = (uc.reg_read(UC_X86_REG_MXCSR))
    CONTEXT[0x78] = (uc.reg_read(UC_X86_REG_RAX))
    CONTEXT[0x80] = (uc.reg_read(UC_X86_REG_RCX))
    CONTEXT[0x88] = (uc.reg_read(UC_X86_REG_RDX))
    CONTEXT[0x90] = (uc.reg_read(UC_X86_REG_RBX))
    CONTEXT[0x98] = (uc.reg_read(UC_X86_REG_RSP))
    CONTEXT[0xa0] = (uc.reg_read(UC_X86_REG_RBP))
    CONTEXT[0xa8] = (uc.reg_read(UC_X86_REG_RSI))
    CONTEXT[0xb0] = (uc.reg_read(UC_X86_REG_RDI))
    CONTEXT[0xb8] = (uc.reg_read(UC_X86_REG_R8))
    CONTEXT[0xc0] = (uc.reg_read(UC_X86_REG_R9))
    CONTEXT[0xc8] = (uc.reg_read(UC_X86_REG_R10))
    CONTEXT[0xd0] = (uc.reg_read(UC_X86_REG_R11))
    CONTEXT[0xd8] = (uc.reg_read(UC_X86_REG_R12))
    CONTEXT[0xe0] = (uc.reg_read(UC_X86_REG_R13))
    CONTEXT[0xe8] = (uc.reg_read(UC_X86_REG_R14))
    CONTEXT[0xf0] = (uc.reg_read(UC_X86_REG_R15))
    CONTEXT[0xf8] = (uc.reg_read(UC_X86_REG_RIP))
    # lets HOPE 0x1408a0000 is open
    context_insts = []
    context_insts.append('stmxcsr dword ptr [0x1408a0034]')
    context_insts.append('mov qword ptr [0x1408a0078], rax')
    context_insts.append('mov rax, rcx')
    context_insts.append('mov qword ptr [0x1408a0080], rax')
    context_insts.append('mov rax, rdx')
    context_insts.append('mov qword ptr [0x1408a0088], rax')
    context_insts.append('mov rax, rbx')
    context_insts.append('mov qword ptr [0x1408a0090], rax')
    context_insts.append('mov rax, rsp')
    context_insts.append('mov qword ptr [0x1408a0098], rax')
    context_insts.append('mov rax, rbp')
    context_insts.append('mov qword ptr [0x1408a00a0], rax')
    context_insts.append('mov rax, rsi')
    context_insts.append('mov qword ptr [0x1408a00a8], rax')
    context_insts.append('mov rax, rdi')
    context_insts.append('mov qword ptr [0x1408a00b0], rax')
    context_insts.append('mov rax, r8')
    context_insts.append('mov qword ptr [0x1408a00b8], rax')
    context_insts.append('mov rax, r9')
    context_insts.append('mov qword ptr [0x1408a00c0], rax')
    context_insts.append('mov rax, r10')
    context_insts.append('mov qword ptr [0x1408a00c8], rax')
    context_insts.append('mov rax, r11')
    context_insts.append('mov qword ptr [0x1408a00d0], rax')
    context_insts.append('mov rax, r12')
    context_insts.append('mov qword ptr [0x1408a00d8], rax')
    context_insts.append('mov rax, r13')
    context_insts.append('mov qword ptr [0x1408a00e0], rax')
    context_insts.append('mov rax, r14')
    context_insts.append('mov qword ptr [0x1408a00e8], rax')
    context_insts.append('mov rax, r15')
    context_insts.append('mov qword ptr [0x1408a00f0], rax')
    context_insts.append('lea rax, [rip]')
    context_insts.append('mov qword ptr [0x1408a00f8], rax')
    # print_red('CONTEXT:')
    # for inst in context_insts:
    #     print_red(inst)

    return context_insts

def reset_regs(uc: Uc, jmp):
    # clean the stack
    uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) - 0x800)
    # clear these registers
    uc.reg_write(UC_X86_REG_RBX, 0)
    uc.reg_write(UC_X86_REG_RDI, 0)
    uc.reg_write(UC_X86_REG_R10, 0)
    uc.reg_write(UC_X86_REG_R11, 0x100000)
    uc.reg_write(UC_X86_REG_R12, 0)
    uc.reg_write(UC_X86_REG_R14, 0)
    # set rax, rip to jmp
    uc.reg_write(UC_X86_REG_RIP, jmp)
    uc.reg_write(UC_X86_REG_RAX, jmp)
    # set r9 to a1000 - 0x28
    uc.reg_write(UC_X86_REG_R9, CONTEXT_BASE + 0x1000 - 0x28)
    # TODO fill in rest, for now we assume other registers will be overwritten
    
    reset_insts = []
    reset_insts.append('mov rbx, 0')
    reset_insts.append('mov rdi, 0')
    reset_insts.append('mov r10, 0')
    reset_insts.append('mov r11, 0x100000')
    reset_insts.append('mov r12, 0')
    reset_insts.append('mov r14, 0')
    reset_insts.append(f'mov rax, 0x{jmp}')
    reset_insts.append(f'mov r9, 0x{CONTEXT_BASE + 0x1000 - 0x28:x}')
    # reset_insts.append('sub rsp, 0x800')
    # reset_insts.append(f'jmp 0x{jmp}')
    return reset_insts

def remap_context_ptr(inst, c_ptr):
    lhs, rhs = inst.op_str.split(', ')
    # if c_ptr in rhs and c_ptr in lhs:
    #     print('WHAT THE SHIT IT APPEARS TWICE', inst)

    # if c_ptr in rhs:
    if 'ptr [' in rhs:
        inner = re.search(r'\[(.*)\]', rhs).group(1)
        parts = inner.split(' ')
        if len(parts) != 1:
            sign = 1 if '+' in inner else -1
            reg, _, offset = parts
            offset = int(offset, 16) * sign
            offset_reg = context_reg_offsets[offset]
            if offset_reg == 'mxcsr':
                lhs_adj = lhs.rstrip('d')
                if lhs_adj.startswith('e'):
                    lhs_adj = 'r' + lhs_adj[1:]
                remapped_insts = [
                    f'mov {lhs_adj}, 0x{MXCSR:x}',
                    f'stmxcsr dword ptr [{lhs_adj}]',
                    'push rax',
                    f'mov eax, dword ptr [0x{MXCSR:x}]',
                    f'mov {lhs}, eax',
                    'pop rax'
                ]
                return remapped_insts

            remapped_inst = f'{inst.mnemonic} {lhs}, {offset_reg}'
            return [remapped_inst]
        else:
            print('WHAT THE F THIS IS BROKEN', inst)
    else:
        if (inner:=(re.search(r'\[(.*)\]', lhs))):
            inner = inner.group(1)
            parts = inner.split(' ')
            if len(parts) != 1:
                sign = 1 if '+' in inner else -1
                reg, _, offset = parts
                offset = int(offset, 16) * sign
                offset_reg = context_reg_offsets[offset]
                remapped_inst = f'{inst.mnemonic} {offset_reg}, {rhs}'
                return [remapped_inst]
            else:
                print('WHAT THE F THIS IS BROKEN', inst)
        else:
            return f'{inst.mnemonic} {inst.op_str}'


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

def unmapped_read(uc: Uc, addr, size):
    print(f'0x{addr:x}: {uc.mem_read(addr, size)}')

insts = []
in_call = False
in_call_insts = []
hlts = 0
def step(uc: Uc, addr, size, user_data):
    global insts, CONTEXT, CONTEXT_PTRS, in_call, in_call_insts, hlts
    inst = uc.mem_read(addr, size)
    inst = next(cs.disasm(inst, addr))

    if insts and f'{inst.mnemonic} {inst.op_str}' == insts[-1]:
        return # duplicate

    # if inst.address > 0x2e4c7f:
    #     print_grey(f'0x{inst.address:x}: {inst.mnemonic} {inst.op_str}')

    if in_call:
        if in_call_insts and in_call_insts[-1].address == inst.address: return # duplicate
        in_call_insts.append(inst)
        # print_grey(f'0x{len(insts):x}: {inst.mnemonic} {inst.op_str}')

        if inst.mnemonic == 'movabs' and 'rax, ' in inst.op_str:
            offset = int(inst.op_str.split(', ')[1], 16)
            if offset > 0x2e4c7f:
                print_red(f'{inst.mnemonic} {inst.op_str}')
            if offset < 0x800000:
                in_call_insts = []

        if inst.mnemonic == 'ret':
            in_call = False
            in_call_insts = []
            return

        if inst.mnemonic == 'jmp':
            in_call = False
            in_call_insts = []
            # jmp to address
            jmp_addr = int(inst.op_str, 16)
            uc.reg_write(UC_X86_REG_RIP, jmp_addr)
            return
        
        if 'mov dword ptr [rip - ' in f'{inst.mnemonic} {inst.op_str}':
            inst = in_call_insts[-2]    
        else:
            if any('mov dword ptr [rip + ' in f'{i.mnemonic} {i.op_str}' for i in in_call_insts[:-1]):
                # print_red('skipping')
                # skip instruction now
                uc.reg_write(UC_X86_REG_RIP, inst.address + inst.size)
                pass
            return
        
        # print_yellow(f'{inst.mnemonic} {inst.op_str}')
        # insts.append(f'{inst.mnemonic} {inst.op_str}')
        
    
    # print(f'0x{inst.address:x}: {inst.mnemonic} {inst.op_str}')
    if inst.mnemonic == 'call':
        in_call = True
        return
    
    elif inst.mnemonic == 'hlt':
        hlts += 1
        insts.append(f'; {hlts} HLT')

        jmp, unwind_codes, frame_reg = parse_unwind_info(make_struct(addr))
        if unwind_codes:
            lifted_unwind = lift_unwind_codes(uc, unwind_codes, frame_reg)
            insts.extend(lifted_unwind)

            # for f in lifted_unwind:
            #     print_yellow(f)

        # set rax, rip to jmp
        uc.reg_write(UC_X86_REG_RIP, jmp)
        uc.reg_write(UC_X86_REG_RAX, jmp)
        # clear context
        CONTEXT_PTRS = []

        # if input('> ') == 'q':
        #     print('quitting')
        #     uc.emu_stop()
        #     uc.reg_write(UC_X86_REG_RIP, -1)
        #     return
        
        # context_insts = pack_context(uc)
        # insts.extend(context_insts)
        # for f in context_insts:z
        #     print_red(f)

        # reset_insts = reset_regs(uc, jmp)
        # insts.extend(reset_insts)
        # for f in reset_insts:
        #     print_red(f)
        
        # if input('> ') == 'q':
        #     print('quitting')
        #     uc.emu_stop()
        #     uc.reg_write(UC_X86_REG_RIP, -1)
        #     return
        # print_red(insts[-1])

    elif inst.mnemonic == 'jmp':
        try:
            jmp = int(inst.op_str, 16)
            uc.reg_write(UC_X86_REG_RIP, jmp)
        except ValueError:
            print_yellow(f'{inst.mnemonic} {inst.op_str}')
            insts.append(f'{inst.mnemonic} {inst.op_str}')
            if inst.address > 0x2d0000 and input("> ") == 'q':
                uc.emu_stop()
                return
            # don't actually execute
            uc.reg_write(UC_X86_REG_RIP, inst.address + inst.size)

    # elif inst.mnemonic == 'mov':
    #     lhs, rhs = inst.op_str.split(', ')
    #     # print(f'lhs: {lhs}, rhs: {rhs}')
    #     if rhs == 'qword ptr [r9 + 0x28]':
    #         # insts.append(f'mov {lhs}, 0x{CONTEXT_BASE:x}')
    #         print_grey(f'{inst.mnemonic} {inst.op_str}')
    #         CONTEXT_PTRS.append(lhs)
    #         return
        
    #     elif 'ptr [' in rhs:
    #         inner = re.search(r'\[(.*)\]', rhs).group(1)
    #         sign = 1 if '+' in inner else -1
    #         parts = inner.split(' ')
    #         if len(parts) != 1:
    #             reg, _, offset = parts
    #             offset = int(offset, 16) * sign

    #             if reg in CONTEXT_PTRS:
    #                 offset_reg = context_reg_offsets[offset]
    #                 print(f'{reg}: {lhs}, {rhs} -> {offset_reg}')
    #                 if input() == 'q': 
    #                     uc.emu_stop()
    #                     return  
    #                 # print(f"{reg} -> {uc.reg_read(uc_reg_map[unwind_reg_map.index(reg)]):x}")
    #                 # uc.reg_write(uc_reg_map[unwind_reg_map.index(lhs)], CONTEXT[offset])
    #                 # print(f'[{offset:x}] -> {CONTEXT[offset]:x}')
    #                 insts.append(f'mov {lhs}, 0x{CONTEXT_BASE + offset:x}')
    #                 insts.append(f'mov {lhs}, qword ptr [{lhs}]')
    #         else:
    #             insts.append(f'{inst.mnemonic} {inst.op_str}')
    #     else:
    #         insts.append(f'{inst.mnemonic} {inst.op_str}')

    #     # print(insts[-1]) 
    #     # don't actually execute 
    #     uc.reg_write(UC_X86_REG_RIP, inst.address + inst.size)        

    elif 'mxcsr' in inst.mnemonic:
        # print_grey(f'{inst.mnemonic} {inst.op_str}')
        # insts.append(f'{inst.mnemonic} {inst.op_str}')

        inner = re.search(r'\[(.*)\]', inst.op_str).group(1)
        offset = int(inner.split(' ')[-1], 16)
        offset_reg = context_reg_offsets[offset]

        if offset_reg == 'mxcsr':
            remapped_insts = ['nop']

        else:
            remapped_insts = [
                'push rax',
                f'mov rax, {offset_reg}',
                f'mov dword ptr [0x{MXCSR:x}], eax',
                f'mov rax, 0x{MXCSR:x}',
                'ldmxcsr dword ptr [rax]',
                'pop rax'
            ]

        # for f in remapped_insts:
        #     print_yellow(f)

        insts.extend(remapped_insts)

        # don't actually execute 
        uc.reg_write(UC_X86_REG_RIP, inst.address + inst.size)

    else:
        if inst.mnemonic == 'mov' and inst.op_str.split(', ')[1] == 'qword ptr [r9 + 0x28]':
            lhs = inst.op_str.split(', ')[0]
            # print_grey(f'{inst.mnemonic} {inst.op_str}')
            CONTEXT_PTRS.append(lhs)
            # print(CONTEXT_PTRS)

        else:
            reg_read, reg_write = inst.regs_access()
            reg_read = [inst.reg_name(r) for r in reg_read]
            reg_write = [inst.reg_name(r) for r in reg_write]

            # print(f'READ: {reg_read}')
            # print(f'WRITE: {reg_write}')
            remapped = False

            for reg_r in reg_read:
                if reg_r in CONTEXT_PTRS:
                    # print_grey(f'{inst.mnemonic} {inst.op_str}')
                    remapped_insts = remap_context_ptr(inst, reg_r)
                    # for remapped_inst in remapped_insts:
                    #     print_red(remapped_inst)
                    insts.extend(remapped_insts)
                    remapped = True
                    break

            for reg_w in reg_write:
                if reg_w in CONTEXT_PTRS:
                    CONTEXT_PTRS.remove(reg_w)
                    
            if not remapped:
                # print(f'{inst.mnemonic} {inst.op_str}')
                insts.append(f'{inst.mnemonic} {inst.op_str}')
                # print(f'read -> {reg_read}')
                # reg_write = [inst.reg_name(r) for r in reg_write]
                # print(f'write -> {reg_write}')
            # for reg in CONTEXT_PTRS:
            #     if f'{reg}' in inst.op_str:
            #         print(f'{inst.mnemonic} {inst.op_str}') 
            #         if ',' in inst.op_str:
            #             lhs, rhs = inst.op_str.split(', ')
            #             if lhs == reg:
            #                 CONTEXT_PTRS.remove(reg)
            #                 break
            #             else:
            #                 print_red(f'{inst.mnemonic} {inst.op_str}')

            # print(f'{inst.mnemonic} {inst.op_str}') 

        # don't actually execute 
        uc.reg_write(UC_X86_REG_RIP, inst.address + inst.size)
    

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
mu.hook_add(UC_HOOK_CODE, step)
mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, unmapped_read)

mu.emu_start(0, length)

with open('dump_lifted.txt', 'w') as f:
    for inst in insts:
        f.write(inst + '\n')
# insts = [i for i in insts if not 'mxcsr' in i]
# extracted = asm('\n'.join(insts))

# extracted += b'\xc3' # ret
# old = open('serpentine.exe', 'rb').read()
# patched = old[:start] + extracted + old[start+len(extracted):]
# open('patched.exe', 'wb').write(patched)
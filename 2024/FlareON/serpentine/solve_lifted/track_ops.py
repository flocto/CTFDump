import re
from time import sleep
import ctypes
from typing import List
import capstone
# from x64dbg import *

parts = open('dump_reparsed.txt', 'r').read().split('cmovne')
flag = b'AAAA0000BBBB1111CCCC2222DDDD3333'
op_dict = {
    'add': '+',
    'sub': '-',
    'xor': '^',
}

def skip_hlts(n):
    for _ in range(n):
        Debug.Run() # will reach a hlt instruction
        # sleep(0.001) 
        Debug.Run() # reach jumpback bp
        # sleep(0.001) 
        Debug.StepIn() # go back
        # sleep(0.001) 

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
# cs.detail = True
def step_until_wanted(inst, after=True):
    while True:
        Debug.StepIn()
        insts = Memory.Read(Register.GetRIP(), 16)
        disas = list(cs.disasm(insts, Register.GetRIP()))
        disas_str = f'{disas[0].mnemonic} {disas[0].op_str}'
        if disas_str.split(',')[0] == inst.split(',')[0]:
            # Gui.InputValue("Enter value")
            if after:
                Debug.StepIn()
            break

def step_until_jmp():
    while True:
        Debug.StepIn()
        if Memory.ReadByte(Register.GetRIP()) == 0xE9:
            break

def clear_test_reg(test_reg):
    match test_reg:
        case 'rax':
            Register.SetCAX(0)
        case 'rbx':
            Register.SetCBX(0)
        case 'rcx':
            Register.SetCCX(0)
        case 'rdx':
            Register.SetCDX(0)
        case 'rsi':
            Register.SetCSI(0)
        case 'rdi':
            Register.SetCDI(0)
        case 'rsp':
            Register.SetCSP(0)
        case 'rbp':
            Register.SetCBP(0)
        case 'rip':
            Register.SetRIP(0)
        case 'r8':
            Register.SetR8(0)
        case 'r9':
            Register.SetR9(0)
        case 'r10':
            Register.SetR10(0)
        case 'r11':
            Register.SetR11(0)
        case 'r12':
            Register.SetR12(0)
        case 'r13':
            Register.SetR13(0)
        case 'r14':
            Register.SetR14(0)
        case 'r15':
            Register.SetR15(0)

def read_reg(reg):
    match reg:
        case 'rax':
            return Register.GetCAX()
        case 'rbx':
            return Register.GetCBX()
        case 'rcx':
            return Register.GetCCX()
        case 'rdx':
            return Register.GetCDX()
        case 'rsi':
            return Register.GetCSI()
        case 'rdi':
            return Register.GetCDI()
        case 'rsp':
            return Register.GetCSP()
        case 'rbp':
            return Register.GetCBP()
        case 'rip':
            return Register.GetRIP()
        case 'r8':
            return Register.GetR8()
        case 'r9':
            return Register.GetR9()
        case 'r10':
            return Register.GetR10()
        case 'r11':
            return Register.GetR11()
        case 'r12':
            return Register.GetR12()
        case 'r13':
            return Register.GetR13()
        case 'r14':
            return Register.GetR14()
        case 'r15':
            return Register.GetR15()

def split_part(part):
    out = []
    chunk = []
    for line in part.split('\n'):
        if line.startswith('==='):
            if chunk:
                out.append(chunk)
                chunk = []
            chunk.append(line)
            # out.append([line])
        else:
            chunk.append(line)
    if chunk:
        out.append(chunk)
    return out

def find_input_offset(chunk):
    shifts = re.findall(r'; UWOP_ALLOC_(?:LARGE|SMALL) ([0-9]+)', chunk)
    if shifts:
        return int(shifts[0])
    return 0

def find_mul_const(chunk):
    lines = chunk.split('\n')
    n = int(lines[2].split()[-1], 16)
    n += int(lines[3].split()[-1], 16)
    n &= 2**64 - 1
    return n

class Term:
    def __init__(self, part):
        # print(part)
        self.input_offset = find_input_offset(part[0])
        self.mul_const = find_mul_const(part[1])
        self.base_const = flag[self.input_offset] * self.mul_const
        self.op = ''
        self.inbetween_op = ''
        self.recovered_const = 0
        # print(f'flag[{input_offset}] * 0x{mul_const:x}')

    def parse_inbetween_op(self, chunk):
        lines = chunk.split('\n')
        assert len(lines) == 3
        # print(lines)
        mnem = lines[-1].split()[0]
        self.inbetween_op = op_dict[mnem]
        self.hlt_idx = int(lines[0].split()[-1])
        self.prev_reg = lines[-1].split()[1][:-1]
        self.wanted_inst = lines[-1].strip()

    def set_op(self, op):
        if self.op == '':
            self.op = op

    def __str__(self):
        s = f'(flag[{self.input_offset}] * 0x{self.mul_const:x} -> 0x{self.base_const:x}) {self.op}'
        if self.recovered_const:
            s += f' 0x{self.recovered_const:x}'
        if self.inbetween_op:
            s = self.inbetween_op + ' ' + s
        return s
    
    def __repr__(self):
        return str(self)

class LastSub:
    def __init__(self, part):
        self.inbetween_op = '-'
        lines = part.split('\n')
        self.hlt_idx = int(lines[0].split()[-1])
        self.prev_reg = lines[-1].split()[1][:-1]
        self.wanted_inst = lines[-2].strip()
        self.base_const = 0
        self.recovered_const = 0

    def set_op(self, op):
        pass

    def __str__(self):
        return f'last_sub {self.hlt_idx}'
    
    def __repr__(self):
        return str(self)

# go to call inner
Debug.Run()
Debug.Run()
Debug.Run()

HLT_IDX = 0
out_file = open('tracked_ops.txt', 'w')
for part in parts[:-1]:
# for part in parts[:5]:
    chunks = split_part(part)
    i = 0

    terms: List[Term] = []
    last_shift = 0
    final_test_hlt = 0
    final_test = 0
    while i < len(chunks):
        chunk = '\n'.join(chunks[i])

        if 'input' in chunk:
            term = Term(['\n'.join(chunks[i + 1])] + ['\n'.join(chunks[i + 2])])
            if terms:
                term.parse_inbetween_op('\n'.join(chunks[i + 3]))
            terms.append(term)
            last_shift = 0

        for op in ['add', 'sub', 'xor']:
            if f'; {op}' in chunk:
                # print(op, terms[-1].op)
                terms[-1].set_op(op)

        if len(terms) == 8:
            if '; sub_carry' in chunk:
                hlt_idx = int(chunks[i][0].split()[-1])
                shifts = re.findall(r'shl (.+, .+)', '\n'.join(chunks[i]))
                # print('sub_carry')
                shift = int(shifts[0].split()[-1], 16)
                if terms[-1].op != 'sub' or shift < last_shift:
                    # print('sub_carry', hlt_idx, shift, last_shift)
                    term = LastSub('\n'.join(chunks[i-1]))
                    terms.append(term)
                # print(shift, last_shift)
                last_shift = shift
        elif len(terms) == 9:
            if 'test' in chunk:
                final_test_hlt = int(chunks[i][0].split()[-1])
                final_test = [inst for inst in chunks[i] if 'test' in inst][0].strip()

        i += 1  

    # print(terms)
    # continue
    # break

    for i, term in enumerate(terms):
        if term.inbetween_op:
            if HLT_IDX < term.hlt_idx:
                skip_hlts(term.hlt_idx - HLT_IDX)
                HLT_IDX = term.hlt_idx
            # step_until_jmp()
            step_until_wanted(term.wanted_inst)
            # print(i, term.hlt_idx, hex(read_reg(term.prev_reg)), term)
            prev_reg = read_reg(term.prev_reg)

            # undo inbetween operation
            match term.inbetween_op:
                case '+':
                    prev_val = prev_reg - term.base_const
                case '-':
                    prev_val = prev_reg + term.base_const
                case '^':
                    prev_val = prev_reg ^ term.base_const

            prev_val = ctypes.c_uint64(prev_val).value
        
            # undo last term operation
            last_term = terms[i-1]
            match last_term.op:
                case 'add':
                    recovered_const = prev_val - last_term.base_const
                case 'sub':
                    recovered_const = last_term.base_const - prev_val
                case 'xor':
                    recovered_const = last_term.base_const ^ prev_val
                case _:
                    pass # none
                
            recovered_const = ctypes.c_uint64(recovered_const).value

            # print(i, term.hlt_idx, term.prev_reg, hex(prev_reg), hex(term.base_const), hex(prev_val), hex(recovered_const), last_term, term)
            
            # prev_reg becomes new value we calculate off of
            term.base_const = prev_reg
            last_term.recovered_const = recovered_const

    # print(final_test_hlt, final_test)
    final_test_reg = final_test.split(', ')[1].strip()
    skip_hlts(final_test_hlt - HLT_IDX)
    HLT_IDX = final_test_hlt
    step_until_wanted(final_test, after=False)
    final_value = read_reg(final_test_reg)
    final_sub = terms[-1].base_const - final_value
    final_sub = ctypes.c_uint64(final_sub).value
    # print([hex(t.recovered_const) for t in terms if t.recovered_const])
    # print(hex(final_sub)) 
    clear_test_reg(final_test_reg)
    # Gui.Refresh()
    # break
    out_file.write(f'{terms[:-1]} 0x{final_sub:x}\n')
    out_file.flush()

# Gui.InputValue("")
#!/usr/bin/env python3

import struct
from enum import Enum, auto

class BPFClass(Enum):
    LD = 0x00
    LDX = 0x01
    ST = 0x02
    STX = 0x03
    ALU = 0x04
    JMP = 0x05
    RET = 0x06
    ALU64 = 0x07
    # These are BPF_JMP32, BPF_ALU32 in more recent kernels
    UNUSED1 = 0x08
    UNUSED2 = 0x09
    # BPF extensions
    MISC = 0xF0

class BPFSize(Enum):
    W = 0x00  # 32-bit
    H = 0x08  # 16-bit
    B = 0x10  # 8-bit
    DW = 0x18  # 64-bit

class BPFMode(Enum):
    IMM = 0x00
    ABS = 0x20
    IND = 0x40
    MEM = 0x60
    LEN = 0x80
    MSH = 0xa0
    XADD = 0xc0

class BPFALU(Enum):
    ADD = 0x00
    SUB = 0x10
    MUL = 0x20
    DIV = 0x30
    OR = 0x40
    AND = 0x50
    LSH = 0x60
    RSH = 0x70
    NEG = 0x80
    MOD = 0x90
    XOR = 0xa0
    MOV = 0xb0
    ARSH = 0xc0
    END = 0xd0

class BPFSource(Enum):
    K = 0x00  # 32-bit immediate
    X = 0x08  # Index register

class BPFJump(Enum):
    JA = 0x00
    JEQ = 0x10
    JGT = 0x20
    JGE = 0x30
    JSET = 0x40
    JNE = 0x50
    JSGT = 0x60
    JSGE = 0x70
    CALL = 0x80
    EXIT = 0x90
    JLT = 0xa0
    JLE = 0xb0
    JSLT = 0xc0
    JSLE = 0xd0

def format_immediate(imm):
    """Format immediate value with ASCII representation if printable."""
    if 32 <= imm <= 126:  # Printable ASCII range
        return f"{imm} ('{chr(imm)}')"
    return f"{imm}"

def decode_instruction(i, instruction):
    """Decode a BPF instruction from a 64-bit integer."""
    # eBPF instruction format: 
    # op:8, dst:4, src:4, off:16, imm:32
    # Extract fields from the instruction
    op = (instruction & 0xFF)
    src_reg = ((instruction >> 8) & 0xF)
    dst_reg = ((instruction >> 12) & 0xF)
    offset = struct.unpack('h', struct.pack('H', (instruction >> 16) & 0xFFFF))[0]  # Signed 16-bit
    imm = struct.unpack('i', struct.pack('I', (instruction >> 32) & 0xFFFFFFFF))[0]  # Signed 32-bit
    # print(f"Decoded instruction: op={op:x}, dst_reg={dst_reg}, src_reg={src_reg}, offset={offset}, imm={imm}")
    
    # Decode opcode
    opcode = op & 0x07  # class
    src_type = op & 0x08  # src
    
    # Extract instruction class
    try:
        bpf_class = BPFClass(opcode)
    except ValueError:
        return f"Unknown instruction class: {opcode:x}"
    
    # Decode instruction based on class
    if bpf_class == BPFClass.ALU or bpf_class == BPFClass.ALU64:
        alu_op = op & 0xf0
        src_type = op & 0x08
        try:
            alu_operation = BPFALU(alu_op)
            src_name = "X" if src_type else "K"
            class_name = "ALU64" if bpf_class == BPFClass.ALU64 else "ALU"
            
            if alu_operation == BPFALU.NEG:
                return f"{alu_operation.name} r{dst_reg}"
            else:
                if src_type:
                    src_val = f"r{src_reg}"
                else:
                    src_val = format_immediate(imm)
                return f"{alu_operation.name} r{dst_reg} {src_val}"
        except ValueError:
            return f"Unknown ALU operation: {alu_op:x}"
    
    elif bpf_class == BPFClass.JMP:
        jmp_op = op & 0xf0
        src_type = op & 0x08
        try:
            jump_operation = BPFJump(jmp_op)
            if jump_operation == BPFJump.CALL:
                return f"CALL {imm}"
            elif jump_operation == BPFJump.EXIT:
                return f"EXIT"
            elif jump_operation == BPFJump.JA:
                return f"JA {offset} ({i + offset})"
            else:
                if src_type:
                    src_val = f"r{src_reg}"
                else:
                    src_val = format_immediate(imm)
                return f"{jump_operation.name} r{dst_reg}, {src_val}, {offset}"
        except ValueError:
            return f"Unknown jump operation: {jmp_op:x}"
    
    elif bpf_class == BPFClass.LD or bpf_class == BPFClass.LDX:
        size = op & 0x18
        mode = op & 0xe0
        try:
            size_name = BPFSize(size).name
            mode_name = BPFMode(mode).name
            class_name = "LD" if bpf_class == BPFClass.LD else "LDX"
            
            if mode == BPFMode.IMM.value:
                # print(src_type, src_reg)
                return f"LD {size_name}/IMM r{dst_reg}, [r{src_reg}]"
            elif mode == BPFMode.MEM.value:
                if bpf_class == BPFClass.LDX:
                    src_desc = f"r{src_reg}"
                else:
                    src_desc = format_immediate(imm)
                return f"{size_name}/MEM r{dst_reg}, [r{src_reg}{'+'+str(offset) if offset else ''}]"
            else:
                val = offset if offset else imm
                return f"{size_name}/{mode_name} r{dst_reg}, {format_immediate(val)}"
        except ValueError:
            return f"Unknown LD/LDX mode or size: mode={mode:x}, size={size:x}"
    
    elif bpf_class == BPFClass.ST or bpf_class == BPFClass.STX:
        size = op & 0x18
        mode = op & 0xe0
        try:
            size_name = BPFSize(size).name
            mode_name = BPFMode(mode).name
            class_name = "ST" if bpf_class == BPFClass.ST else "STX"
            
            if mode == BPFMode.MEM.value:
                if bpf_class == BPFClass.ST:
                    value = format_immediate(imm)
                else:
                    value = f"r{src_reg}"
                return f"{size_name}/MEM [r{dst_reg}{'+'+str(offset) if offset else ''}], {value}"
            elif mode == BPFMode.XADD.value:
                return f"XADD [r{dst_reg}{'+'+str(offset) if offset else ''}], r{src_reg}"
            else:
                val = offset if offset else imm
                return f"ST {size_name}/{mode_name} [r{dst_reg}], {format_immediate(val)}"
        except ValueError:
            return f"Unknown ST/STX mode or size: mode={mode:x}, size={size:x}"
    
    else:
        return f"Unhandled instruction class: {bpf_class.name}, op={op:x}, dst={dst_reg}, src={src_reg}, off={offset}, imm={imm}"

def main():
    with open('program.bpf', 'r') as f:
        instructions = [int(line.strip()) for line in f.readlines() if line.strip()]
    
    print("Disassembled BPF program:")
    print("-------------------------")
    
    for i, instr in enumerate(instructions):
        decoded = decode_instruction(i, instr)
        print(f"{i:4d}: {instr:16x} {decoded}")

if __name__ == "__main__":
    main()
import struct

program = bytes.fromhex(open('program.hex', 'r').read().strip())
program = struct.unpack('<' + 'Q' * (len(program) // 8), program)

insts = {
    0x2815: ('load_const', 1),
    0x2bad: ('load_mem', 1),
    0x2f4b: ('dup', 0),
    0x3403: ('store_mem', 1),
    0x380e: ('read_input', 0),
    0x3a63: ('print', 0),
    0x3ca9: ('add', 0),
    0x4249: ('subtract', 0),
    0x47eb: ('mul', 0),
    0x4d19: ('sub_4d19', 0),
    0x5256: ('rotate_left', 0),
    0x581b: ('rotate_right', 0),
    0x5e14: ('sub_5e14', 0),
    0x6390: ('bitwise_and', 0),
    0x68f7: ('bitwise_or', 0),
    0x6e5e: ('bitwise_xor', 0),
    0x73c5: ('jmp', 1),
    0x7511: ('jeq', 1),
    0x7b82: ('jne', 1),
    0x81f3: ('jlt', 1),
    0x885d: ('jle', 1),
    0x8ec7: ('jgt', 1),
    0x9531: ('jge', 1),
    0x9b9b: ('exit', 0),
    0x9ba9: ('system', 0),
}

disas = []
pc = 0
while pc < len(program):
    inst = program[pc]
    if inst not in insts:
        disas.append(f'0x{inst:04x}: unknown')
        pc += 1
        continue

    name, size = insts[inst]
    args = program[pc + 1:pc + 1 + size]
    if size == 1:
        args_str = f'0x{args[0]:02x}'
    else:
        args_str = ', '.join(f'0x{arg:02x}' for arg in args)

    disas.append(f'{pc:03x}: {name}'.ljust(20) + args_str)
    pc += 1 + size

with open('disas.txt', 'w') as f:
    for line in disas:
        f.write(line + '\n')
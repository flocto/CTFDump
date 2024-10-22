data = open('svm_revenge', 'rb').read()

start = 0x3060
end = 0x38a0

def jump_table(op):
    jmp_table = [
	    0xfffff38f, 0xfffff344, 0xfffff290, 0xfffff2fd,
	    0xfffff2d3, 0xfffff2b8
    ]
    op = jmp_table[op] + 0x2004
    op = op & 0xffffffff

    match op:
        case 0x1294:
            op = 'push_reg'
        case 0x12bc:
            op = 'push_imm'
        case 0x12d7:
            op = 'pop_reg'
        case 0x1301:
            op = 'add'
        case 0x1348:
            op = 'mul'

    return op

data = data[start:end]

def parse_insts(data):
    ops = []
    for i in range(0, len(data), 2):
        op, arg = data[i:i+2]
        # op = jump_table(op)
        op = [
            'mul',
            'push_reg',
            'add',
            'pop_reg',
            'push_imm'
        ][op - 1]

        ops.append((op, arg))
    
    return ops


ops = parse_insts(data)

if __name__ == '__main__':
    for i, (op, arg) in enumerate(ops):
        if op != 'add' and op != 'mul':
            print(f'{i//2:04x}: {op:8} {arg:02x}')
        else:
            print(f'{i//2:04x}: {op:8}')

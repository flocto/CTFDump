data = open('printf_patched', 'rb').read()

start = 0x2008
length = 0x168a2
data = data[start:start+length].decode()
def parse(data):
    insts = data.split('%')[1:]

    opcodes = {
        'A': 'read',
        'B': 'print',
        'D': 'pop',
        'E': 'pop',
        'F': 'add',
        'G': 'sub',
        'H': 'mul',
        'I': 'div',
        'J': 'mod',
        'K': 'xor',
        'M': 'push_const',
        'N': 'push_reg',
        'X': 'end',
    }

    parsed = []
    read_seen = False
    for inst in insts:
        op = opcodes[inst[-1]]
        arg = inst[:-1]
        arg2 = None
        if arg[-1] not in '.0123456789':
            spec = 'Lhl'
            arg2 = spec.index(arg[-1])
            arg = arg[:-1]

        if op == 'read':
            # print(f'{op:10}')
            read_seen = True
            parsed.append((op, None))
            continue
        elif op == 'print':
            # print(f'{op:10}')
            parsed.append((op, None))
            continue
        elif op == 'end':
            # print(f'{op:10}')
            parsed.append((op, None))
            continue

        elif op != 'push_const':
            # print(f'{op:10} {arg2}')
            if arg2 is None:
                spec = "# -+'"
                arg2 = spec.index(arg[2]) + 3
                # print(arg[2], op, arg2)
            # if read_seen:
            #     print(inst, op, arg2)
            parsed.append((op, arg2))
            continue

        arg = arg.split('$')[1]
        arg_l, arg_h = arg.split('.')
        arg_l, arg_h = int(arg_l), int(arg_h)
        arg = arg_l << 32 | arg_h
        
        # if read_seen:
        #     print(inst, op, arg)
        parsed.append((op, arg))
    return parsed

if __name__ == '__main__':
    parsed = parse(data)
    # for op, arg in parsed:
    #     if isinstance(arg, int):
    #         print(f'{op:10} {arg:18x}')
    #     else:
    #         print(f'{op:10}')
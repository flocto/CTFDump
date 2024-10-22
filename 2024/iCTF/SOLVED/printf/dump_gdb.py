import gdb

gdb.execute("run <<< ictf{AAAAAA}")

def rbs(n):
    # find index of most significant bit
    return n.bit_length() - 1

offsets = {
    0x11a8: 'read',
    0x11e5: 'print',
    0x1212: 'push_const',
    0x125b: 'push_reg',
    0x12ce: 'pop',
    0x133a: 'add',
    0x13be: 'sub',
    0x1446: 'mul',
    0x14cb: 'div',
    0x1555: 'mod',
    0x15df: 'xor',
    0x1663: 'end',
}

base = 0x555555554000
read_seen = False
while True:
    try:
        rip = int(gdb.parse_and_eval("$rip")) - base
        op = offsets.get(rip)
        arg = None
        # print(hex(rip), op)
        if op == 'end':
            break
        elif op in ['read', 'print']:
            if op == 'read':
                read_seen = True
            pass
        elif op == 'push_const':
            arg = gdb.execute("x/gx $rsi", to_string=True).split()[-1]
            arg = int(arg, 16)
        else:
            arg = gdb.execute("x/gx $rsi+8", to_string=True).split()[-1]
            arg = int(arg, 16) >> 32
            arg = rbs(arg)
        
        # print(op, hex(arg)[2:].zfill(16))
        if read_seen:
            if arg is None:
                print(f'{op:10}')
            else:
                print(f'{op:10} {arg:16x}')

        gdb.execute("c")
    except gdb.error:
        break
import binaryninja as bn
from binaryninja import BinaryView, BinaryViewType
from string import printable
import struct
printable = printable.encode()
# printable = b'_ 0123456789abcdef'

bv: BinaryView = eval("bv")

flag_funcs = []
for func in bv.functions:
    if func.name == 'flag_4b10f3b631b53f504f56e51c98ad8dac':
        continue
    if func.name.startswith("flag_"):
        flag_funcs.append(func)

def handle_func(func):
    add_str = ""
    xor_data = b''
    add_const = 0
    for inst in f.hlil.instructions:
        text = str(inst)
        # print(text)
        if 'strcpy' in text:
            add_str = text.split('"')[1]
        elif 'memcpy' in text:
            xor_data = text.split('"')[1]
            xor_data = ('b"' + xor_data + '"').replace('\\t', '\\x09').replace('\\n', '\\x0a').replace('\\r', '\\x0d')
            print(f"Function: {func.name}, xor_data: {xor_data}")
            xor_data = eval(xor_data)
        elif 'var_1c = ' in text:
            add_const = int(text.split(' ')[-1], 0)

    # print(f"add_str: {add_str}")
    # print(f"xor_data: {xor_data}")
    # print(f"add_const: {add_const}")
    for c in add_str.encode():
        add_const += c
    add_const &= 0xFFFFFFFF
    xor_data = struct.unpack(f'<{len(xor_data) // 4}I', xor_data)
    # print(f"Function: {func.name}, add_const: {add_const}, xor_data: {xor_data}")
    xor_data = bytes([(add_const & 0xff) ^ (c & 0xff) for c in xor_data])
    # print(f"Function: {func.name}, xor_data: {xor_data}")
    if all(c in printable for c in xor_data):
        print(f"Function: {func.name}, flag: {xor_data}")

    return xor_data.startswith(b'bca')
for f in flag_funcs:
    if handle_func(f):
        break
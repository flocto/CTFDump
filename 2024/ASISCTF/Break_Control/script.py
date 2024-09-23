import gdb
import struct

def parse_hex(data):
    out = b''
    for line in data.splitlines():
        for part in line.split()[1:]:
            out += int(part, 16).to_bytes(4, 'little')

    return out

# get 1248 int

out = gdb.execute('x/1248wx 0x000055555555c480', to_string=True)
out = parse_hex(out)

bits = struct.unpack('<1248I', out)
print(bits)

dat = bytes([int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)])
print(dat)
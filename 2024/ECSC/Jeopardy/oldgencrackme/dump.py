import gdb
import struct 

def parse_hex(data):
    dat = b''
    for row in data.split('\n'):
        for part in row.split()[1:]:
            dat += int(part, 16).to_bytes(4, 'little')

    return dat

dat = parse_hex(gdb.execute('x/300wx $rax+0x100000', to_string=True))
nums = [struct.unpack('<I', dat[i:i+4])[0] for i in range(0, len(dat), 4)]
print(nums)
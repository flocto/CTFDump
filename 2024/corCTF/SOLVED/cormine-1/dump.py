data = open('cormine1.cms', 'rb').read()
data = data[6:]
i = 0

mask = 0xffffffffffffffff
def read_serialized():
    global i
    res = 0
    shift = 0
    buf = b''
    while True:
        b = data[i]
        buf += bytes([b])
        i += 1
        res |= (b & 0x7f) << shift
        shift += 7

        if b & 0x80 == 0:
            print(buf.hex())
            if b & 0x40:
                return res | (mask << shift) & mask
            return res 
        
for _ in range(10):
    x, y, z = read_serialized(), read_serialized(), read_serialized()
    x, y, z = [d & 0xffffffff for d in [x, y, z]]
    print(hex(x), hex(y), hex(z))
    i += 1 # skip type

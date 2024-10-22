from Crypto.Cipher import ARC4
import ctypes
libc = ctypes.CDLL('libc.so.6')

buf = bytearray([0] * 0x100)
i = 0
j1, j2 = 0, 0

def rc4_init():
    global i, j1, j2, buf
    i = j1 = j2 = 0
    for i in range(0x100):
        buf[i] = i

def rc4_key(key, key_len):
    global i, j1, j2, buf
    # i = j1 = 0
    for key_i in range(0, len(key), 0x100):
        _key = key[key_i:key_i+0x100]

        for i in range(0x100):
            c_i = buf[i]
            j1 += c_i + _key[i % key_len]
            j1 %= 0x100
            buf[i] = buf[j1]
            buf[j1] = c_i
    i = 0
        
def rc4_stream(dat: bytearray, len):
    global i, j1, j2, buf
    # i = j2 = 0
    for dat_i in range(len):
        i += 1
        i %= 0x100
        c_i = buf[i]
        j2 += c_i
        j2 %= 0x100
        buf[i] = buf[j2]
        buf[j2] = c_i
        dat[dat_i] ^= buf[(buf[i] + buf[j2]) % 0x100]

key = b'%\xf7\xa1\xfcPTU!h\xde\xba{\' \x8f\x8ay\xbe\'\x9d^$\xe1\x130\x97\x8c\xe3\x03k\xdb(b}$\xb3\xd2y\xd4:X\x8e\xb6\x80\xafF\x0b(\x042\xc5cW\xa7w\x88>\x03kAoGj\xd1\xc4\x8e\x84\x96\x08Y\xd1a\xe8\x88\xe1\x97\xce\xec\xbf\xd3\x1f\x857w-\xaf\xffl\xb3j\xae\"\xb1\x18\xf4v\xa7x\x0c\xb0\xd2\xde\x11\xbaf\xf3R5\xe0\x12\t\xff\x98Av\xc6\xf0v2\xa3\xe0\xe1\xc5\x92\xfa\xb9\x08\xa12\x14R\x05\xf3d\xc0ZW\x12\x8f7%\x997\xbd\xda\xae\x84\xca$\xb6n\x04\x984\x96\x92\xee\x9f4 \xb4\x86&\xa7\xea\xe6\x01B\xf9\x91z\x1e*\xb1\xdc\x04_`\xcf\x83\x17=\x88\xafq\x1fB_\xbev\x80r\xfd\xa7\x1a\xe8\x8d\x1b*\x86\xac\xa4\xa5\xd7V\x81\xdb\xb5\xe2\xab9\xfa\xe8\xc2\xaaZ\xe1\xec\xba\xa0c;\x13a\xe2-IoIt\xf6\xf6\x19\x9b\xcdo\x1d\xa9%\x00T_\xfa=!\xa4\x98\x02\x91R\xa3\xf4\x8e\xb6Up'
print(len(key))
rc4_init()
rc4_key(key, len(key))

DATS = [
    b'\xf6\xdc\xad\xe4k\xa7\xb9\xb2@\x00\xb0 \x06\xd6\x82\xc4\x9f0\xb7\x8fQ\xc5s\xba&~\xe1\x06\x13\x02\xdd*rPC\x15\x84X=\xbd>u\x8a\x95\xd6\x81@\x1c\xd3e\x86?\x17`\xcd&0\x92\x84\xcc\x8e\xad\x03\xc0\x16',
    b'\x03',
    b'\xb9n\x1b\xbf\xe6\xbb\x95|',
    b'e,\x94',
    b'F\xf2\x9d\xc3\xd1\xeb\x0f\xf9\x16\xc6\xe6\x02c\xfda',
    b'\x9c',
    b'x:\xecA\x9cC4\x8b\xd7\xe9g\xa3\x95\xaa\xc2\xd8\x01P\xb3\x1b|\xf3',
]
DATS = [bytearray(d) for d in DATS]

for d in DATS:
    rc4_stream(d, len(d))
    print(d, hex(len(d)))

rc4_key(DATS[-1], len(DATS[-1]))

DATS = [
    b'\xe1AAa\xcb\xf7\xd2\xb7\xc0\xea\xbd@\\\x8c|l\xef\xdb\x11\x9c\'\"'
]
DATS = [bytearray(d) for d in DATS]

for d in DATS:
    rc4_stream(d, len(d))
    print(d, hex(len(d)))
from tqdm import trange
from hashlib import sha512
from Crypto.Cipher import ChaCha20

p = 0xc90102faa48f18b5eac1f76bb40a1b9fb0d841712bbe3e5576a7a56976c2baeca47809765283aa078583e1e65172a3fd
print(p, int(p).bit_length())
a = 0xa079db08ea2470350c182487b50f7707dd46a58a1d160ff79297dcc9bfad6cfc96a81c4a97564118a40331fe0fc1327f
b = 0x9f939c02a7bd7fc263a4cce416f4c575f28d0c1315c4f0c282fca6709a5f9f7f9c251c9eede9eb1baa31602167fa5380
gx = 0x087b5fe3ae6dcfb0e074b40f6208c8f6de4f4f0679d6933796d3b9bd659704fb85452f041fff14cf0e9aa7e45544f9d8
gy = 0x127425c1d330ed537663e87459eaa1b1b53edfe305f6a79b184b3180033aab190eb9aa003e02e9dbf6d593c5e3b08182
n = 30937339651019945892244794266256713890440922455872051984762505561763526780311616863989511376879697740787911484829297

F = GF(p)
E = EllipticCurve(F, [a, b])

G = E((gx, gy))

xorkey = 0x133713371337133713371337133713371337133713371337133713371337133713371337133713371337133713371337

def encrypt_thing(dat):
    return dat ^^ xorkey

def parse_bytearray(dat):
    return int.from_bytes(dat, 'big')

def pack_bytearray(n):
    n = int(n)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

x1 = bytes.fromhex(
    '0a6c559073da49754e9ad9846a72954745e4f2921213eccda4b1422e2fdd646fc7e28389c7c2e51a591e0147e2ebe7ae')
y1 = bytes.fromhex(
    '264022daf8c7676a1b2720917b82999d42cd1878d31bc57b6db17b9705c7ff2404cbbf13cbdb8c096621634045293922')

x2 = bytes.fromhex(
    'a0d2eba817e38b03cd063227bd32e353880818893ab02378d7db3c71c5c725c6bba0934b5d5e2d3ca6fa89ffbb374c31')
y2 = bytes.fromhex(
    '96a35eaf2a5e0b430021de361aa58f8015981ffd0d9824b50af23b5ccf16fa4e323483602d0754534d2e7a8aaf8174dc')

x1, y1 = encrypt_thing(parse_bytearray(x1)), encrypt_thing(parse_bytearray(y1))
x2, y2 = encrypt_thing(parse_bytearray(x2)), encrypt_thing(parse_bytearray(y2))
p1 = E((x1, y1))
p2 = E((x2, y2))

A_secret = 168606034648973740214207039875253762473

shared = A_secret * p2

hsh = sha512(pack_bytearray(shared.xy()[0])).digest()
key = hsh[:32]
nonce = hsh[32:40]
print(key, nonce)

enc = b"\xf2r\xd5L1\x86\x0f?\xbdC\xda>\xe3%\x86\xdf\xd7\xc5\x0c\xea\x1cJ\xa0d\xc3Z\x7fn:\xb0%\x84A\xac\x15\x85\xc3bV\xde\xa8<\xac\x93\x00z\x0c:)\x86O\x8e(_\xfay\xc8\xebC\x97m[X\x7f\x8f5\xe6\x99Tq\x16\xfc\xb1\xd2\xcd\xbb\xa9y\xc9\x89\x99\x8caI\x0b\xce9\xdaWp\x11\xe0\xd7n\xc8\xeb\x0b\x82Y3\x1d\xef\x13\xeem\x86r>\xac\x9f\x04(\x92N\xe7\xf8A\x1dLp\x1bM\x9e+7\x93\xf6\x11}\xd3\r\xac\xba,\xae`\x0b_2\xce\xa1\x93\xe0\xdec\xd7\t\x83\x8b\xd6\xa7\xfd5\xed\xf0\xfc\x80+\x15\x18lz\x1b\x1aG]\xaf\x94\xae@\xf6\xbb\x81\xaf\xce\xdcJ\xfb\x15\x8aQ(\xc2\x8c\x91\xcdz\x88W\xd1*f\x1a\xca\xec\xae\xc8\xd2z|\xf2j\x17'6\x855\xa4N/9\x17\xed\tD}\xedyr\x19\xc9f\xef=\xd5pZ<2\xbd\xb1q\n\xe3\xb8\x7f\xe6fi\xe0\xb4do\xc4\x16\xc3\x99\xc3\xa4\xfe\x1e\xdc\n>\xc5\x82{\x84\xdbZy\xb8\x164\xe7\xc3\xaf\xe5(\xa4\xda\x15E{cx\x157=N\xdc\xac!Y\xd0V\xf5\x98\x1fq\xc7\xea\x1b]\x8b\x1e_\x06\xfc\x83\xb1\xde\xf3\x8coNiN7\x06A.\xab\xf5N;oM\x19\xe8\xefF\xb0N9\x9f,\x8e\xce\x84\x17\xfa@\x08\xbcT\xe4\x1e\xf7\x01\xfe\xe7N\x80\xe8\xdf\xb5KH\x7f\x9b.:'\x7f\xa2\x89\xcfl\xb8\xdf\x98l\xdd8~4*\xc9\xf5(m\xa1\x1c\xa2x@\x84\\\xa6\x8d\x13\x94\xbe*M=M|\x82\xe51\xb6\xda\xc6.\xf1\xad\x8d\xc1\xf6\x0by&^\xd0\xde\xaa1\xdd\xd2\xd5:\xa9\xfd\x93CF8\x10\xf3\xe2#$\x066kHAS3\xd4\xb8\xac3m@\x86\xef\xa0\xf1^nY\r\x1e\xc0o6"

cipher = ChaCha20.new(key=key, nonce=nonce)

dec = cipher.decrypt(enc)
print(dec)
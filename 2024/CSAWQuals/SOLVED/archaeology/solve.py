def washing_machine(msg: bytearray):
    b = msg[0]
    for i in range(1, len(msg)):
        msg[i] ^= b
        b = msg[i]

    for i in range(0, len(msg) >> 1):
        msg[i], msg[len(msg) - i - 1] = msg[len(msg) - i - 1], msg[i]
    
    return msg

sbox = [
	0x48, 0x5c, 0xbc, 0x97, 0x81, 0x91, 0x60, 0xad, 0x94, 0xcb, 0x92, 0x39, 0x1a, 0x0f, 0x30, 0x2d,
	0x45, 0xde, 0x14, 0xa2, 0x08, 0x57, 0xb6, 0xae, 0x76, 0x8e, 0x87, 0x15, 0x0c, 0xe7, 0x62, 0xc8,
	0x58, 0x29, 0x6d, 0xc9, 0xa7, 0xbe, 0x04, 0x49, 0x05, 0xfa, 0x75, 0x9f, 0xfd, 0x95, 0xbb, 0x5b,
	0x79, 0xbf, 0xda, 0xeb, 0x21, 0x9b, 0xa5, 0x82, 0x3a, 0x3e, 0xb9, 0x99, 0xf0, 0xf5, 0x6b, 0x06,
	0xfc, 0xaf, 0xf2, 0xb0, 0x78, 0x86, 0xcf, 0xd4, 0x83, 0x59, 0x00, 0x4a, 0xb5, 0xfe, 0xab, 0x3d,
	0xc7, 0x8c, 0xe3, 0xc3, 0xe5, 0x03, 0x5a, 0x1d, 0x9d, 0x1f, 0x0a, 0x56, 0xc0, 0xba, 0x43, 0x25,
	0x77, 0x24, 0x7c, 0xa6, 0xdf, 0xf1, 0x4b, 0x44, 0xff, 0x4c, 0xaa, 0xc1, 0x69, 0xf9, 0x38, 0x88,
	0x9a, 0xa4, 0xe6, 0x10, 0xdc, 0xea, 0x68, 0x8d, 0x5f, 0x63, 0xbd, 0x8b, 0xf3, 0x7e, 0xdb, 0x73,
	0x5d, 0x65, 0x67, 0xa1, 0x72, 0xd8, 0xb1, 0x1b, 0x9e, 0x84, 0x16, 0x32, 0xe1, 0xf4, 0xef, 0x93,
	0xac, 0x74, 0x36, 0x8f, 0xcc, 0x61, 0x0d, 0x35, 0x12, 0xdd, 0x4e, 0xc4, 0x64, 0x3f, 0x09, 0x70,
	0x2a, 0xfb, 0xc5, 0x85, 0x3b, 0x1c, 0x50, 0x19, 0xd5, 0xe9, 0x47, 0x0b, 0xe2, 0xca, 0xc6, 0xf7,
	0xb2, 0xd6, 0xf8, 0x11, 0x54, 0x6e, 0x90, 0xc2, 0xec, 0x96, 0x51, 0xd7, 0xe8, 0x31, 0x80, 0x7d,
	0x18, 0x34, 0xb7, 0x02, 0xa0, 0x7a, 0xb3, 0xd0, 0x46, 0x66, 0x37, 0x1e, 0x7b, 0x42, 0x6c, 0x17,
	0xd9, 0x33, 0x2b, 0x22, 0xce, 0xa9, 0x7f, 0xb4, 0x07, 0x6a, 0x41, 0x40, 0x26, 0x2f, 0xa8, 0xcd,
	0x71, 0xb8, 0x53, 0x13, 0x5e, 0xf6, 0xe0, 0x52, 0x4f, 0x6f, 0xe4, 0x89, 0x3c, 0x9c, 0xa3, 0x8a,
	0x4d, 0x28, 0x0e, 0xd3, 0xd2, 0x98, 0xee, 0x2c, 0x2e, 0xed, 0x27, 0x20, 0x01, 0x23, 0x55, 0xd1,
]

def unwashing_machine(msg: bytearray):
    for i in range(0, len(msg) >> 1):
        msg[i], msg[len(msg) - i - 1] = msg[len(msg) - i - 1], msg[i]

    b = msg[0]
    for i in range(1, len(msg)):
        next_b = msg[i]
        msg[i] ^= b
        b = next_b

    return msg

def run_vm(c):
    # runs vm on one character c
    init = [0xaa, 0xbb, 0xcc, 0xdd, 0xee]

    for j in range(10):
        c = ((c >> 3) | (c << 5)) & 0xff
        c = sbox[c]
        c ^= init[j % 5]
        c = ((c << 3) | (c >> 5)) & 0xff
    
    return c

enc_map = {
    i: run_vm(i) for i in range(256)
}

dec_map = {
    v: k for k, v in enc_map.items()
}

glyphs = open('hieroglyphs.txt', 'r').read().strip().split('\n')
glyphs = {
    glyph: i for i, glyph in enumerate(glyphs)
}

enc = open('flag.txt', 'r').read()
enc = bytearray([glyphs[glyph] for glyph in enc])
print(enc, len(enc))

unwash = unwashing_machine(enc)
dec = bytearray([dec_map[c] for c in unwash])
unwash2 = unwashing_machine(dec)

print(unwash2, len(unwash2))
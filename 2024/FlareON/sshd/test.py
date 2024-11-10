# uint64_t flip_endian(char* arg1 @ rax)

#     char* rcx = arg1
#     arg1.b = *rcx
#     void* b
#     b.b = rcx[1]
#     void* c
#     c.b = rcx[2]
#     void* d
#     d.b = rcx[3]
#     return zx.q(0 | zx.d(arg1.b) | zx.d(b.b) << 8 | zx.d(c.b) << 0x10 | zx.d(d.b) << 0x18)


def flip_endian(arg1):
    rcx = arg1
    arg1 = rcx[0]
    b = rcx[1]
    c = rcx[2]
    d = rcx[3]
    return 0 | arg1 | b << 8 | c << 0x10 | d << 0x18

test = b'expa'
print(test, test.hex(), hex(flip_endian(test)))
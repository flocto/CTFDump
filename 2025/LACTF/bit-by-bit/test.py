from ctypes import *
from structs import *
libc = CDLL('libc.so.6')

server_name = b'NS\x11REV\x0eLAC\x0eTF'
server_name = bytes([i ^ 0x20 for i in server_name])
print(server_name)

len_query = b'lfh\'~jd;tz}\x0fPA*'
len_query = bytes([x ^ (i * 3) for i, x in enumerate(len_query)])
print(len_query)

# add server_name as DNS server for res_query later

libc.gethostbyname.restype = POINTER(hostent)
host = libc.gethostbyname(c_char_p(server_name))

libc.__res_state.restype = POINTER(res_state)
res = libc.__res_state()

# 000013f2                    int64_t h_length = sx.q(hostent->h_length)
# 00001402                    rax_7->nscount = 1
# 00001418                    memcpy(&rax_7->nsaddr_list[0].sin_addr, *hostent->h_addr_list, h_length)
h_length = host.contents.h_length
res.contents.nscount = 1
res.contents.nsaddr_list[0].sin_addr.s_addr = int.from_bytes(host.contents.h_addr_list[0], 'little')

# 0x200 char buf
buf = b'\x00' * 0x200

res = libc.res_query(c_char_p(len_query), 0x1, 0x10, buf, 0x200)
print(res, buf)

libresolv = CDLL('libresolv.so.2')
handle = ns_msg()

libresolv.ns_initparse(buf, res, byref(handle))

record = ns_rr()
libresolv.ns_parserr(byref(handle), 1, 0, byref(record))

rdata = record.rdata
n = rdata[0]
nptr = rdata[1:1+n]
length = int(bytes(nptr))
print("len =", length)

query = b'4u?ctg?}pr?ew\x11'
query_template = bytes([x ^ 0x11 for i, x in enumerate(query)])
print(query_template)

def make_query(query):
    buf = b'\x00' * 0x200
    res = libc.res_query(c_char_p(query), 0x1, 0x10, buf, 0x200)

    handle = ns_msg()
    libresolv.ns_initparse(buf, res, byref(handle))
    record = ns_rr()
    libresolv.ns_parserr(byref(handle), 1, 0, byref(record))

    rdata = record.rdata
    n = rdata[0]
    nptr = rdata[1:1+n]
    return bytes(nptr)

res = [0] * length
cur = 7678622
while True:
    try:
        query = query_template % cur
        out = make_query(query)
        nxt, stuff = out.split(b';')
        print(out)
        cur = int(nxt)

        if stuff:
            i, x = map(int, stuff.split(b','))
            print(i, x)
            byt_idx = i // 8
            bit_idx = i % 8
            res[byt_idx] |= x << bit_idx

        if cur == -1:
            break
    except KeyboardInterrupt:
        print(cur)
        break           

print(bytes(res))
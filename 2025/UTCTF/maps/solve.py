from pwn import process

def guess(test):
    p = process(['./chal'], level='error')
    p.sendlineafter(b'! ', test)
    out = p.recvline().strip()
    p.close()
    return out

expected = b'4934849349493674935749360493664940249346493534935849348493574936549351493644937449348493464936449365493744935349360493464935449364493574935749374493494935349358493594935449404'

alpha = b'utflag{}_abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

known = b''
while len(known) < 35:
    n = len(known) + 1
    for c in alpha:
        test = known + bytes([c])
        out = guess(test)
        # print(test, out)
        if out[:5 * n] == expected[:5 * n]:
            known += bytes([c])
            print(known)
            break

print(known)

# blocks = [int(expected[i:i+5]) for i in range(0, len(expected), 5)]
# x = blocks[0] - b'u'[0]

# dec = bytes([b - x for b in blocks])
# print(dec)
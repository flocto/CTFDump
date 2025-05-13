def e(m, k):
    r = []
    r += [m[0]^(sum(k)&0o377)]
    for _, i in enumerate(m[1:]):
        k = e(k, [m[_]])
        r += [i^(sum(k)&0o377)]
    return bytes(r)

def e_sym(m, k):
    r = []
    r += [m[0]^(sum(k)&0o377)]
    for _, i in enumerate(m[1:]):
        k = e_sym(k, [m[_]])
        r += [i^(sum(k)&0o377)]
    return r


e2 = open('chall.flag', 'rb')
I = b''
while True:
    i = e2.read(3)
    if (i := int.from_bytes(i, 'big')) == 0:
        break
    print(i)
    I += e2.read(i)

tst = b'ABCDEEFF'
r = e(tst, tst)
# print(e(tst, tst))

# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Nice Progress! I wonder if there is a better way to do this
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

I = locals()
l = dict(I)
i = marshal.dumps
l2 = str([dir(_) for _ in l.values()]).encode()

def e(m):
    return bytes([a ^ b for a, b in zip(m, m[len(m) // 2:])])
import traceback
l2 = e(e(l2))
l2 += str(l['marshal']).encode() + l['c']
l2 = e(l2) + i(e.__code__.co_code) + (tb := traceback.format_stack()[-1].encode())
l2 = e(l2) + i(inspect.getsource.__code__.co_code) + i(l['e'].__code__.co_code)
l2 = e(e(e(e(e(l2) + e(i(open(__file__).read()))))))
e = open('chall.flag', 'rb')
I = b''
while True:
    i = e.read(3)
    if (i := int.from_bytes(i, 'big')) == 0:
        break
    I += l['e'](e.read(i), l2)
    l2 = l['e'](l2, l2)
exec(marshal.loads(I))
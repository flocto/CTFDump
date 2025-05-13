from pwn import remote
import itertools
# nc chall.lac.tf 31179
r = remote('chall.lac.tf', int(31179))

p = 171687271187362402858253153317226779412519708415758861260173615154794651529095285554559087769129718750696204276854381696836947720354758929262422945910586370154930700427498878225153794722572909742395687687136063410003254320613429926120729809300639276228416026933793038009939497928563523775713932771366072739767
P = GF(p)
PP.<s> = PolynomialRing(P)

r.recvline()
s_pow = eval(r.recvline().decode().split(': ')[1])
alpha_pow = eval(r.recvline().decode().split(': ')[1])
print(s_pow)
print(alpha_pow)

r.recvline()
coefs = eval(r.recvline().decode().split(': ')[1])

for _ in range(3):
    r.sendlineafter(b'> ', b'2')

target = eval(r.recvline().decode().split('was ')[1])

print(f"target: {target}")

f = sum([coefs[i] * s^(7 - i) for i in range(8)])
f = f - target
f = f.monic()
print(f"monic: {f}")
rts = f.roots()
print(f'roots: {r}')
s = rts[-1][0]
print(s)

assert sum(coefs[i] * pow(s, 7-i, p) for i in range(8)) %p == target

coefs = eval(r.recvline_contains(b'target polynomial: ').decode().split(': ')[1])
# print(coefs)

ts = int(sum(coefs[i] * pow(s, 7-i, p) for i in range(8)) % p )
print(f"ts: {ts}")

d = pow(ts, -1, p-1)
print(f"d: {d}")
for f, fa in zip(s_pow, alpha_pow):
    try:
        h = pow(int(f), int(d), int(p))
        print(f"h: {h}")
        print(f"f: {f}")
        assert pow(h, int(ts), int(p)) == f
        
        r.sendlineafter(b'> ', str(f).encode())
        r.sendlineafter(b'> ', str(h).encode())
        r.sendlineafter(b'> ', str(fa).encode())
        break
    except Exception as e:
        print(e)
        pass

r.interactive()


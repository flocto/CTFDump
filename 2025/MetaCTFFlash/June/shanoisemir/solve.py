from pwn import remote, process
from sage.all import *
# nc kubenode.mctf.io 31007
primes = []
rems = []

for _ in range(32):
    r = remote('kubenode.mctf.io', '31007')
    # r = process(['python3', 'src.py'], level='error')
    polys = []

    p = int(r.recvline().strip().split()[-1].decode())
    N = 5
    for i in range(N):
        r.sendlineafter(b'Share (yes/no) > ', b'yes')
        r.sendlineafter(b'Amount > ', b'5')
        # share_sets.append(eval(r.recvline().strip().decode()))
        x, ys = eval(r.recvline().strip().decode())
        polys.append((x, min(ys)))
    r.close()

    R = PolynomialRing(GF(p), ['c0', 'c1', 'c2', 'c3', 'c4'])
    coeffs = R.gens()[:5]
    equations = []
    for x_val, y_val in polys:
        eq = sum(coeff * (x_val ** i) for i, coeff in enumerate(coeffs)) 
        equations.append(eq - y_val)

    I = R.ideal(equations)
    gb = I.groebner_basis()

    # Extract solution for a0 (the secret)
    for poly in gb:
        if poly.degree() == 1 and len(poly.variables()) == 1 and coeffs[0] in poly.variables():
            secret_val = -poly.constant_coefficient() / poly.coefficient(coeffs[0])
            secret_val = int(secret_val) % p
            print(f"Secret (decimal): {secret_val}")
            primes.append(p)
            rems.append(secret_val)
            break

print("Primes:", primes)
print("Rems:", rems)

flag = crt(rems, primes)
flag = int(flag)
flag = flag.to_bytes((flag.bit_length() + 7) // 8, 'big')
print("Flag:", flag)
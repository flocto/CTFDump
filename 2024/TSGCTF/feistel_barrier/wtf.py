from Crypto.Util.number import getStrongPrime

p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
phi = (p-1)*(q-1)
e = 65537
d = pow(e, -1, phi)

m = 31337
c = pow(m, e, n)
print(c)

k = pow(2, e, n)
print(k)

c_2 = (c * k) % n
print(c_2)

c_2 = c_2.to_bytes((c_2.bit_length() + 7) // 8, 'big')

# on server
s_m = pow(int.from_bytes(c_2, 'big'), d, n)
em = s_m.to_bytes(128, 'big')

ct = int.from_bytes(em, 'big')
ct = (ct * (pow(2, -1, n))) % n
print(ct)
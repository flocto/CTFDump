import random

def dot(a,b,p):
    assert len(a) == len(b)
    return sum([(a[i]*b[i])%p for i in range(len(a))])%p

def count_on_cipher(ciphertexts,p):
    result = [sum([ciphertexts[i][j] for i in range(len(ciphertexts))])%p for j in range(len(ciphertexts[0]))]
    return result

n = 1024
m = 2048
k = 128
p = 2**k
q = m*2
assert p > q

secret_key = [random.randint(0,1) for _ in range(n)]
disagree = random.randint(0,m-1)
ciphertexts = []

for i in range(m):
    a = [random.randint(0,p-1) for _ in range(n)]
    if i == disagree:
        b = dot(secret_key,a,p)
        ciphertexts.append(a+[b])
    else:
        b = (1*(p//q) + dot(secret_key,a,p))%p
        ciphertexts.append(a+[b])


agree_num_cipher = count_on_cipher(ciphertexts,p)
agree_num = (agree_num_cipher[-1] - dot(secret_key,agree_num_cipher[:-1],p))%p
print(agree_num//(p//q))
assert agree_num//(p//q) == m-1



flag = "TSGCTF{dummy}"
encrypted_flag = []
for i in range(len(flag)):
    a = [random.randint(0,p-1) for _ in range(n)]
    nosie = random.randint(0,p//q-1)
    pt = (ord(flag[i])*(p//q))%p
    b = (pt + dot(secret_key,a,p) + nosie)%p
    encrypted_flag.append(a+[b])


print("n =",n)
print("m =",m)
print("p =",p)
print("q =",q)
print("ciphertexts =",ciphertexts)
print("encrypted_flag =",encrypted_flag)

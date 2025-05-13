from pwn import *
import ctypes
from sage.all import *
from functools import cache

# r = process("./main")
# ]nc chall.polygl0ts.ch 9070
r = remote("chall.polygl0ts.ch", 9070)

@cache
def f(n):
    if n < 0x20:
        return 0
    arr = [0] * 0x20
    arr[0x1f] = 1
    j = 1
    i = 0

    # all uint64s
    for itr in range(0x20, n + 1):
        tmp = j - arr[i]
        tmp = ctypes.c_uint64(tmp).value
        arr[i] = j
        arr[i] = ctypes.c_uint64(arr[i]).value
        j += tmp
        j = ctypes.c_uint64(j).value
        i = (i + 1) & 0x1f
    
    return arr[(i + 0x1f) & 0x1f]


@cache
def fast_f(n):
    if n < 0x40:
        return f(n)
    
    p = 2**64
    P = Integers(p)
    k = 33

    # Transition matrix M: a_n = a_{n-1} + a_{n-k}
    M = Matrix(P, k, k)

    # Fill in shift: M[i][i+1] = 1 for i = 0..k-2
    for i in range(k - 1):
        M[i, i+1] = 1

    # F_n = 2F_{n-1} - F_{n-k}
    M[k-1, 0] = -1
    M[k-1, k-1] = 2

    vec = [1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648]
    v0 = vector(P, vec)

    if n < k:
        return v0[n]
    Mn = M**(n - 63)
    return (Mn * v0)[k - 1]


line = r.recvline_contains(b'What is f(')
n = int(line.split(b'(')[1].split(b')')[0])
x = 1 << (n - 32)
print(f"f({n}) = {x}")
r.sendlineafter(b'Your answer: ', str(x).encode())

line = r.recvline_contains(b'What is f(')
n = int(line.split(b'(')[1].split(b')')[0])
x = fast_f(n)
print(f"f({n}) = {x}")
r.sendlineafter(b'Your answer: ', str(x).encode())

line = r.recvline_contains(b'What is f(')
n = int(line.split(b'(')[1].split(b')')[0])
x = fast_f(n)
print(f"f({n}) = {x}")
r.sendlineafter(b'Your answer: ', str(x).encode())

r.interactive()
import ctypes
from sage.all import *
from functools import cache

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

    M = Matrix(P, k, k)

    for i in range(k - 1):
        M[i, i+1] = 1

    M[k-1, 0] = -1
    M[k-1, k-1] = 2

    vec = [1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648]
    v0 = vector(P, vec)
    
    Mn = M**(n - 63)
    return (Mn * v0)[k - 1]


for i in range(255, 1000):
    x = f(i)
    # px = f(i-1)
    # ppx = f(i - 33)
    # print(i, x, px, ppx, 2 * px - x)
    fx = fast_f(i)
    print(i, x, fx, x - fx)

# f(100)

# n = 70
# x = f(n)
# exp_x = 1 << (n - 32)
# diff = x - exp_x
# print(diff)

# for i in range(0x20, 300):
#     exp_x = 1 << (i - 32)
#     x = f(i)
#     if x != exp_x:
#         print("Error at i =", i)
#         print("Expected:", exp_x)
#         print("Got:", x)
#         break
#     else:
#         print('same', i, x, exp_x)


# for i in range(64, 70):
#     exp_x = 1 << (i - 32)
#     x = f(i)
#     if x != exp_x:
#         print("Expected:", exp_x)
#         print("Got:", x)
#         diff = x - exp_x
#         print("Diff:", diff)
 
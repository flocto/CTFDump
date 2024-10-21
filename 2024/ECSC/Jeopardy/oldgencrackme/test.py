import gdb
import random
from sympy import isprime, nextprime
from math import gcd, lcm

alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def to_base36(n):
    out = ''
    while n:
        out += alpha[n % 36]
        n //= 36
    return out

def from_base36(s):
    out = 0
    for c in s:
        out *= 36
        out += alpha.index(c)
    return out

while True:
    out = []
    used_x = []
    used_primes = []
    used_y = []
    # while True:
    #         x = random.randint(0, 36**4)
    #         y = x ^ 0xffffff

    #         if isprime(x) and x not in used_x and x != 2 and x not in [3, 5, 7, 13, 17, 241]:
    #             used_x.append(x)
    #             used_primes.append(x)
    #             break

    # while True:
    #     # if isprime(y) and y not in used_x and y != 11 and x % 11 == 0:
    #     x = random.randint(0, 36**4 // g)
    #     g = used_primes[-1]
    #     if isprime(x):
    #         # if any(gcd(x, u) != 1 for u in used_y):
    #         #     continue
    #         used_primes.append(x)
    #         x = x * g
    #         y = x ^ 0xffffff
    #         if any(gcd(x, u) != 1 for u in used_y):
    #             continue
    #         used_x.append(x)
    #         used_y.append(y)
    #         print(x, y)
    #         # out.append(to_base36(x).ljust(4, '0'))
    #         if len(used_x) == 200:
    #             break

        # if isprime(g := gcd(x, y)) and g > 3:
            # print(gcd(x, y))
            # used_x.add(x)
            # out.append(to_base36(x).ljust(4, '0'))
            # if len(out) == 200:
            #     break

    # 3, 5, 7, 13, 17, 241
    # for p in [3, 5, 7, 13, 17, 241]:
    #     used_x.add(p)
    #     out.append(to_base36(p).ljust(4, '0'))

    while True:
        x = random.randint(0, 36**4)
        y = x ^ 0xffffff

        if all(gcd(y, u) == 1 for u in used_y) and all(gcd(x, u) == 1 for u in used_x):
            print(x, y)
            used_x.append(x)
            used_y.append(y)
            if len(used_x) == 200:
                break

    #         # out.append(to_base36(x).ljust(4, '0'))
            # if len(out) == 200:
            #     break
    #     if x not in used_x and all(gcd(x, u) == 1 for u in used_y) and all(gcd(y, u) == 1 for u in used_x):
    #         used_x.add(x)
    #         out.append(to_base36(x).ljust(4, '0'))
    #         if len(out) == 200:
    #             break

        # if len(out) < 100:
        #     if x % 11 == 0 and y % 11 != 0 and gcd(x, y) == 1 and x not in used_x:
        #         if y % 19 == 0 and x % 19 != 0:
        #             used_x.add(x)
        #             out.append(to_base36(x).ljust(4, '0'))
        #             if len(out) == 200:
        #                 break
        # else:
        # if x % 113 == 0 and y % 113 != 0 and gcd(x, y) == 1 and x not in used_x:
        #     if y % 11 == 0 and x % 11 != 0:
        # if isprime(x) and x not in used_x and x > 100 and y % 11 == 0:   
            # print(x, y)
        # if isprime(y) and y not in used_x and y != 11 and x % 11 == 0:

        # p = gcd(x, y)
        # if len(used) == 6 and p == 1:
        #     out.append(to_base36(x).ljust(4, '0'))
        #     if len(out) == 200:
        #         break
        # elif p not in used and isprime(p):
        #     # for u in used:
        #     #     if gcd(p, u) != 1:
        #     #         break
        #     # else:
        #         print(p, hex(x), hex(y))
        #         used.add(p)
        #         out.append(to_base36(x).ljust(4, '0'))
        #         if len(out) == 200:
        #             break
        # elif p == 2:
        #     used.add(2)
        #     out.append(to_base36(x))
        #     if len(out) == 200:
        #         break

    # while True:
    #     x = random.randint(0, 36**4)
    #     y = x ^ 0xffffff

    #     if isprime(gcd(x, y)):
    #         out.append(to_base36(x).ljust(4, '0'))
    #         break

    # print('-'.join(out))

    # prod = lcm(*used_x)
    # print(prod)

    print(len(used_x))

    out = [to_base36(x).ljust(4, '0') for x in sorted(used_x)]

    inp = '-'.join(out)
    print(inp)

    gdb.execute(f'r <<< {inp}')
    gdb.execute('info b')

    # if rax == 1, stop
    # if gdb.parse_and_eval('$rax') == 1:
    #     print(inp)
    #     print(inp)
    #     print(inp)
    #     print(inp)
    #     break
    # break
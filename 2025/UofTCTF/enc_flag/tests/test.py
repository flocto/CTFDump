MOD = 2147483647
seed = 19175311
r = []
r.append(seed)

for i in range(1, 31):
    r.append((16807 * r[i-1]) % MOD)

print(r)

for i in range(31, 34):
    r.append(r[i-31])

for i in range(34, 344):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

for i in range(344, 1000):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

r = [x >> 1 for x in r[344:]]
print(r[:31])
# for i in range(10):
#     print(r[i])

def factor(x):
    return [i for i in range(1, x+1) if x % i == 0]
vals = []
for i in range(1, 617):
    facs = factor(i)
    print(i, facs)
    vals.append((i, len(facs)))

vals = sorted(vals, key=lambda x: x[1])
vals = [v for v in vals if v[1] == vals[-1][1]]
print(vals)